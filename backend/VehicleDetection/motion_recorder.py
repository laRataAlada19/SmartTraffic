import cv2
import time
import os

OUTPUT_DIR = "/Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/backend/VehicleDetection/videos/cam1"
os.makedirs(OUTPUT_DIR, exist_ok=True)
VIDEO_DURATION = 10  
FPS = 20  
MIN_CONTOUR_AREA = 2000 
MOTION_THRESHOLD = 5  
FRAME_SKIP = 5  

def detect_motion_and_record():
    cap = cv2.VideoCapture(2) 
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    motion_frames = 0
    frame_counter = 0

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
                output_path = f"{OUTPUT_DIR}/video_{timestamp}.mp4"
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

        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_motion_and_record()
