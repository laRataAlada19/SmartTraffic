import os
import subprocess
import re
import time
import cv2

# Caminhos e configurações
MAPPING_FILE = "camera_map.txt"
OUTPUT_BASE_DIR = "./videos"
VIDEO_DURATION = 10  # segundos
FPS = 20
MIN_CONTOUR_AREA = 2000
MOTION_THRESHOLD = 5
FRAME_SKIP = 5

def listar_cameras_ffmpeg():
    """Executa o comando ffmpeg para listar dispositivos AVFoundation e guarda mapeamento."""
    print("A listar câmaras com ffmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        output = result.stderr  # a listagem aparece no stderr
    except Exception as e:
        print("Erro ao correr ffmpeg:", e)
        return {}

    cameras = {}
    # Regex para linhas tipo: [AVFoundation input device @ 0x7fbf9c406d80] [0] FaceTime HD Camera
    for line in output.splitlines():
        m = re.search(r'\[(\d+)\] (.+)', line)
        if m:
            index = int(m.group(1))
            name = m.group(2).strip()
            cameras[name] = index

    # Guarda mapeamento num ficheiro simples
    with open(MAPPING_FILE, "w") as f:
        for name, index in cameras.items():
            f.write(f"{name}={index}\n")

    print(f"Mapeamento guardado em {MAPPING_FILE}")
    return cameras

def ler_mapeamento():
    """Lê o ficheiro camera_map.txt e devolve dict name->index"""
    if not os.path.exists(MAPPING_FILE):
        return {}

    cameras = {}
    with open(MAPPING_FILE, "r") as f:
        for line in f:
            if "=" in line:
                name, index = line.strip().split("=", 1)
                cameras[name] = int(index)
    return cameras

def detect_motion_and_record(camera_index, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Erro ao abrir a câmara no índice {camera_index}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    motion_frames = 0
    frame_counter = 0

    print(f"Iniciado monitorização da câmara {camera_index}, grava vídeos em {output_dir}")

    while True:
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
                output_path = os.path.join(output_dir, f"video_{timestamp}.mp4")
                out = cv2.VideoWriter(output_path, fourcc, FPS, (frame_width, frame_height))

                start_time = time.time()
                while time.time() - start_time < VIDEO_DURATION:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)

                out.release()
                print(f"Vídeo salvo em: {output_path}")
                motion_frames = 0
        else:
            motion_frames = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Monitorização encerrada pelo utilizador.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Se o ficheiro de mapeamento não existe, gera-o
    cameras = ler_mapeamento()
    if not cameras:
        cameras = listar_cameras_ffmpeg()
        if not cameras:
            print("Nenhuma câmara encontrada. Sai.")
            exit(1)

    print("\nCâmaras detectadas e seus índices:")
    for name, index in cameras.items():
        print(f"- {name} => índice {index}")

    # Exemplo: procura um nome parcial para o iPhone via Camo (ajusta aqui para o teu dispositivo)
    nome_camera_procura = "iPhone de Francisco"  
    camera_index = None
    for name, index in cameras.items():
        if nome_camera_procura.lower() in name.lower():
            camera_index = index
            camera_name = name
            break

    if camera_index is None:
        print(f"Não foi encontrada a câmara com '{nome_camera_procura}' no nome.")
        print("Usa um dos índices detetados manualmente.")
        exit(1)

    print(f"\nUsando a câmara '{camera_name}' no índice {camera_index}")

    pasta_saida = os.path.join(OUTPUT_BASE_DIR, camera_name.replace(" ", "_"))
    detect_motion_and_record(camera_index, pasta_saida)
