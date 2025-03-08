from ultralytics import YOLO
import cv2
from collections import defaultdict, deque
import numpy as np
import argparse
import time
import torch

# Configurações iniciais
parser = argparse.ArgumentParser(description="Contador de veículos com YOLO e tracking")
parser.add_argument('--video', type=str, default='4.mp4', help='Caminho para o vídeo')
parser.add_argument('--max_track_history', type=int, default=30, help='Número máximo de frames no tracking')
args = parser.parse_args()

# Carregar modelo
def load_model():
    return YOLO('yolov8n.pt')

def display_results(detected_vehicles, class_counter):
    print("\n==== FINAL RESULTS ====")
    print(f"Total Unique Detections: {len(detected_vehicles)}")
    
    for class_name, count in class_counter.items():
        print(f"Class: {class_name}, Count: {count}")

    print("========================\n")

# para eliminar deteçoes duplicadas em varias frames consecutivas, medindo a sobreposição entre as caixas delimitadoras.
def compute_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    box1_x1, box1_y1, box1_x2, box1_y2 = x1 - w1 / 2, y1 - h1 / 2, x1 + w1 / 2, y1 + h1 / 2
    box2_x1, box2_y1, box2_x2, box2_y2 = x2 - w2 / 2, y2 - h2 / 2, x2 + w2 / 2, y2 + h2 / 2

    inter_x1 = max(box1_x1, box2_x1)
    inter_y1 = max(box1_y1, box2_y1)
    inter_x2 = min(box1_x2, box2_x2)
    inter_y2 = min(box1_y2, box2_y2)

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    box1_area = (box1_x2 - box1_x1) * (box1_y2 - box1_y1)
    box2_area = (box2_x2 - box2_x1) * (box2_y2 - box2_y1)

    return inter_area / (box1_area + box2_area - inter_area + 1e-6) # retorna IoU, ou seja, a interseção sobre a união. Idealmente, o valor deve ser 0 pois não há sobreposição, e 1 se as caixas são idênticas, ou seja, idealmente sobrepostas.

# verifica se a nova caixa delimitadora é uma duplicata de uma caixa delimitadora já detectada. Se a IoU entre a nova caixa e uma caixa já detectada for maior que 0.5, consideramos a nova caixa como uma duplicata.
def is_duplicate(detected_vehicles, new_box):
    for old_box in detected_vehicles.values():
        if compute_iou(old_box, new_box) > 0.5:
            return True
    return False

def process_frame(frame, model, detected_vehicles, class_counter, track_history, max_track_history):
    results = model.track(frame, persist=True)
    if results and results[0].boxes and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        conf_list = results[0].boxes.conf.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bike'}
        for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
            if model.names[int(cls)] not in vehicle_classes or conf < 0.7:
                continue

            if track_id not in detected_vehicles and not is_duplicate(detected_vehicles, box):
                detected_vehicles[track_id] = box
                class_name = model.names[int(cls)]
                class_counter[class_name] += 1

            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame
    return frame

# Inicializar variáveis
model = load_model()
cap = cv2.VideoCapture(args.video)
class_counter = defaultdict(int)
detected_vehicles = {}  # Agora um dicionário
track_history = defaultdict(lambda: deque(maxlen=args.max_track_history))

prev_time = time.time()

# Loop principal
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = process_frame(frame, model, detected_vehicles, class_counter, track_history, args.max_track_history)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

display_results(detected_vehicles, class_counter)