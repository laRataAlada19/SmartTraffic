from ultralytics import YOLO
import cv2
from collections import defaultdict, deque
import numpy as np
import argparse
import time

# Configurações iniciais
parser = argparse.ArgumentParser(description="Contador de veículos com YOLO e tracking")
parser.add_argument('--video', type=str, default='Small.mp4', help='Caminho para o vídeo')
parser.add_argument('--max_track_history', type=int, default=30, help='Número máximo de frames no tracking')
args = parser.parse_args()

# Carregar modelo
def load_model():
    return YOLO('yolov8n.pt')

# Processar frame
def process_frame(frame, model, detected_vehicles, class_counter, track_history, max_track_history):
    results = model.track(frame, persist=True)
    if results and results[0].boxes and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        conf_list = results[0].boxes.conf.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
            x, y, w, h = box
            class_id = int(cls)

            if track_id not in detected_vehicles:
                detected_vehicles.add(track_id)
                class_name = model.names[class_id]
                class_counter[class_name] += 1

            track = track_history[track_id]
            track.append((float(x), float(y)))
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame
    return frame

# Mostrar resultados
def display_results(detected_vehicles, class_counter, class_relevant):
    total_detections_wanted = sum(class_counter[class_name] for class_name in class_counter if class_name in class_relevant)
    
    print(f"Total Detection: {len(detected_vehicles)}")
    for class_name, count in class_counter.items():
        if class_name in class_relevant:
            print(f"Classe: {class_name}, Contagem: {count}")
    print(f"Total Detections Wanted: {total_detections_wanted}")

# Inicializar variáveis
model = load_model()
cap = cv2.VideoCapture(args.video)
class_counter = defaultdict(int)
detected_vehicles = set()
track_history = defaultdict(lambda: deque(maxlen=args.max_track_history))
class_relevant = {'car', 'truck', 'bus', 'moto', 'bike'}

prev_time = time.time()

# Loop principal
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame, model, detected_vehicles, class_counter, track_history, args.max_track_history)

    # Calcular FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Exibir resultados finais
display_results(detected_vehicles, class_counter, class_relevant)
