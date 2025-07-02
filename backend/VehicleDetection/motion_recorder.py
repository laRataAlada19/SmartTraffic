import os
import subprocess
import re
import time
import cv2
from threading import Event


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAPPING_FILE = os.path.join(SCRIPT_DIR, "camera_map.txt")

OUTPUT_BASE_DIR = "./videos"
VIDEO_DURATION = 10 
FPS = 20
MIN_CONTOUR_AREA = 2000
MOTION_THRESHOLD = 5
FRAME_SKIP = 5

def listar_cameras_ffmpeg():
    print("A listar câmaras com ffmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        output = result.stderr
    except Exception as e:
        print("Erro ao correr ffmpeg:", e)
        return {}

    cameras = {}
    for line in output.splitlines():
        m = re.search(r'\[(\d+)\] (.+)', line)
        if m:
            index = int(m.group(1))
            name = m.group(2).strip()
            cameras[name] = index

    with open(MAPPING_FILE, "w") as f:
        for name, index in cameras.items():
            f.write(f"{name}={index}\n")

    print(f"Mapeamento guardado em {MAPPING_FILE}")
    return cameras

def ler_mapeamento():
    if not os.path.exists(MAPPING_FILE):
        return {}
    cameras = {}
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                nome, idx = line.strip().split("=", 1)
                cameras[nome.strip()] = int(idx.strip())
    return cameras


def detect_motion_and_record(camera_index, output_dir, stop_event):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print(f"Erro ao abrir a câmara no índice {camera_index}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    motion_frames = 0
    frame_counter = 0

    print(f"Iniciado monitorização da câmara {camera_index}, grava vídeos em {output_dir}")

    while not stop_event.is_set():
        frame_counter += 1
        if frame_counter % FRAME_SKIP != 0:
            continue

        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        if not ret:
            break

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        relevant_contours = [
            c for c in contours
            if cv2.contourArea(c) > MIN_CONTOUR_AREA and 0.5 < cv2.boundingRect(c)[2] / cv2.boundingRect(c)[3] < 3
        ]

        if len(relevant_contours) > 0:
            motion_frames += 1
            if motion_frames >= MOTION_THRESHOLD:
                print("Movimento detectado! Gravando vídeo...")
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                output_path = os.path.join(output_dir, f"video_{timestamp}.mp4")  # Use o diretório da localização
                out = cv2.VideoWriter(output_path, fourcc, FPS, (frame_width, frame_height))

                start_time = time.time()
                while time.time() - start_time < VIDEO_DURATION:
                    if stop_event.is_set():
                        print("Parando gravação...")
                        break
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)

                out.release()
                print(f"Vídeo salvo em: {output_path}")

    cap.release()

if __name__ == "__main__":
    print("Este ficheiro é agora um módulo. Usa-o via camera_server.py")
