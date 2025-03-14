from ultralytics import YOLO
import cv2
from collections import defaultdict, deque
import numpy as np
import argparse
import time
import torch
from trackers.byte_tracker import BYTETracker  # Import ByteTrack

# Configurações iniciais
parser = argparse.ArgumentParser(description="Contador de veículos com YOLO e ByteTrack")
parser.add_argument('--video', type=str, default='4.mp4', help='Caminho para o vídeo')
args = parser.parse_args()

# Carregar modelo YOLOv8
def load_model():
    return YOLO('yolov8n.pt')

# Inicializar ByteTrack
tracker = BYTETracker()

def display_results(detected_vehicles, class_counter):
    print("\n==== FINAL RESULTS ====")
    print(f"Total Unique Detections: {len(detected_vehicles)}")
    for class_name, count in class_counter.items():
        print(f"Class: {class_name}, Count: {count}")
    print("========================\n")
    for old_box in detected_vehicles.values():
        if compute_iou(old_box, new_box) > 0.5:
            return True
    return False

# não é necessário usar o compute_iou e is_duplicate pois o ByteTrack já faz isso nativamente. 
# o ByteTrack usa o Hungarian Algorithm para associar as caixas delimitadoras de detecção em diferentes frames, e também lida com a eliminação de duplicados

def process_frame(frame, model, tracker, detected_vehicles, class_counter, track_history, max_track_history):
    # nao é necessário usar o método track pois o ByteTrack já faz isso nativamente
    # nao é necessario usar persist=True pois o ByteTrack já faz isso nativamente, ao manter o rastreamento dos IDs entre frames
    results = model(frame) 
    if results and results[0].boxes:
        boxes = results[0].boxes.xywh.cpu().numpy()
        conf_list = results[0].boxes.conf.cpu().numpy()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        # Filtrar apenas veículos
        vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bike'}
        detections = []
        for box, cls, conf in zip(boxes, clss, conf_list):
            class_name = model.names[int(cls)]
            if class_name in vehicle_classes and conf > 0.7:
                detections.append(np.append(box, conf))

        detections = np.array(detections) if len(detections) > 0 else np.empty((0, 5)) # transforam o detectionsnum array numpy se houver detecções, caso contrário, cria um array vazio
        tracks = tracker.update(detections)  # Aplicar ByteTrack

        for track in tracks:
            track_id, x, y, w, h = int(track[4]), track[0], track[1], track[2], track[3]
            if track_id not in detected_vehicles:
                detected_vehicles[track_id] = (x, y, w, h)
                class_counter[class_name] += 1

            #desenha a trajetoria do veiculo, ao usar o track_history para armazenar as coordenadas do centro da caixa delimitadora do veiculo em cada frame.
            track_history[track_id].append((int(x), int(y)))
            points = np.hstack(track_history[track_id]).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame
    return frame

# Inicializar variáveis
model = load_model()
cap = cv2.VideoCapture(args.video)
class_counter = defaultdict(int)
detected_vehicles = {}
track_history = defaultdict(lambda: deque(maxlen=30))
prev_time = time.time()

# Loop principal
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = process_frame(frame, model, tracker, detected_vehicles, class_counter, track_history, 30)
    
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

#source myenv/bin/activate 
#python test_ByteTrack.py --video vid4.mp4