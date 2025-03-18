from ultralytics import YOLO
import cv2
from collections import defaultdict, deque
import numpy as np
import time
import torch
import re

video_files = ["1.mp4", "2.mp4", "3.mp4", "4.mp4", "5.mp4"]
total_class_counter = defaultdict(int)

ground_truth = {
    "1.mp4": {"car": 37, "motorcycle": 1},
    "2.mp4": {"car": 205, "truck": 27, "motorcycle": 3},
    "3.mp4": {"car": 11, "motorcycle": 4, "bike": 2, "truck": 3},
    "4.mp4": {"car": 59, "motorcycle": 68, "truck": 3},
    "5.mp4": {"car": 33, "bus": 1, "truck": 1}
}

# Carregar modelo
def load_model():
    return YOLO('yolov8n.pt')

#deal with saving results to a file
def clean_file(file):
    with open(file, "w") as f:
        f.write("")

    print(f"File cleaned: {file}")
def save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter, output_file="results.txt"):
    with open(output_file, "a") as f:  # Open in append mode to keep results from multiple videos
        f.write(f"\n==== RESULTS FOR {video_file} ====\n")
        f.write(f"Total Unique Detections: {len(detected_vehicles)}\n")
        
        for class_name, count in class_counter.items():
            f.write(f"Class: {class_name}, Count: {count}\n")
            total_class_counter[class_name] += count  # Update total count for each class

        f.write("========================\n\n")

    print(f"Results saved to {output_file}")
def save_total_counts(total_class_counter, output_file="results.txt"):
    with open(output_file, "a") as f:
        f.write("\n==== TOTAL COUNT FOR ALL VIDEOS ====\n")
        for class_name, total_count in total_class_counter.items():
            f.write(f"Class: {class_name}, Total Count: {total_count}\n")
        f.write("========================\n\n")
def load_predictions_from_file(filename="results.txt"):
    predictions = {}
    current_video = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            # Identificar o início de um novo vídeo
            match = re.match(r"==== RESULTS FOR (.+) ====", line)
            if match:
                current_video = match.group(1)
                predictions[current_video] = {}
                continue

            # Ler contagens por classe
            match = re.match(r"Class: (\w+), Count: (\d+)", line)
            if match and current_video:
                class_name, count = match.groups()
                predictions[current_video][class_name] = int(count)

    return predictions
def save_stats_to_file(mape_results, class_mape_results, filename="results.txt"):
    with open(filename, "a") as f:
        #MAPE
        f.write("\n=== MAPE por Vídeo ===\n")
        for video, mape_value in mape_results.items():
            f.write(f"{video}: {mape_value:.2f}%\n")
        f.write("\n=== MAPE por Classe ===\n")
        for cls, mape_value in class_mape_results.items():
            f.write(f"{cls}: {mape_value:.2f}%\n")

#estatisticas
def calculate_mape(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    mask = actual > 0  # Evita divisão por zero (considera apenas classes presentes no ground truth)
    
    if np.any(mask):
        return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100
    return None  # Retorna None se não houver valores reais para comparar

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

# Processa cada frame do vídeo, rastreando os veículos e a sua trajetória
def process_frame(frame, model, detected_vehicles, class_counter, track_history):
    # persist=True para manter o rastreamento de objetos entre frames
    results = model.track(frame, persist=True)
    if results and results[0].boxes and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        conf_list = results[0].boxes.conf.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bike'}
        for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
            if model.names[int(cls)] not in vehicle_classes or conf < 0.6:
                continue

            if track_id not in detected_vehicles and not is_duplicate(detected_vehicles, box):
                detected_vehicles[track_id] = box
                class_name = model.names[int(cls)]
                class_counter[class_name] += 1

            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))

            #desenha a trajetoria do veiculo, ao usar o track_history para armazenar as coordenadas do centro da caixa delimitadora do veiculo em cada frame.
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2)) 
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame
    return frame

# Inicializar modelo
model = load_model()
clean_file("results.txt")

for video_file in video_files:
    print(f"Processing: {video_file}")
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print(f"Erro ao abrir {video_file}")
        continue  # Pula para o próximo vídeo

    # Reset tracking variables for each new video
    class_counter = defaultdict(int)
    detected_vehicles = {}  
    track_history = defaultdict(lambda: deque(maxlen=30))
    prev_time = time.time()

    prevFrame = None  # Reset Optical Flow frame

    # Properly reset tracker for Ultralytics model
    if hasattr(model, 'model'):
        model.model.tracker = None  # Ultralytics tracker reset

    # Get initial video resolution (if needed)
    ret, first_frame = cap.read()
    if not ret:
        print(f"Erro ao ler o primeiro frame de {video_file}")
        cap.release()
        continue
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to start

    # Define target frame size (adjust as needed)
    target_size = (640, 480)  # Example size

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None:
            break  # Se o frame não for válido, encerra o loop

        # Resize frame to target size to ensure consistency
        frame = cv2.resize(frame, target_size)

        # Ensure prevFrame matches size
        if prevFrame is None:
            prevFrame = frame.copy()
        elif prevFrame.shape != frame.shape:
            prevFrame = cv2.resize(prevFrame, (frame.shape[1], frame.shape[0]))

        # Process frame
        frame = process_frame(frame, model, detected_vehicles, class_counter, track_history)

        # Calculate FPS
        curr_time = time.time()
        fps = 1 / max(curr_time - prev_time, 1e-6)
        prev_time = curr_time

        # Display FPS
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  

        prevFrame = frame.copy()  # Update previous frame

    cap.release()
    cv2.destroyAllWindows()
    
    save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter)

save_total_counts(total_class_counter)

model_predictions = load_predictions_from_file()

# Calcular MAPE por vídeo (somente classes do ground truth)
mape_results = {}
for video, actual_counts in ground_truth.items():
    predicted_counts = model_predictions.get(video, {})
    
    # Filtrar apenas classes presentes no ground truth
    all_classes = set(actual_counts.keys())
    
    actual_values = [actual_counts.get(cls, 0) for cls in all_classes]
    predicted_values = [predicted_counts.get(cls, 0) for cls in all_classes]

    mape_results[video] = calculate_mape(actual_values, predicted_values)

# Calcular MAPE por classe (evitando distorções por classes ausentes)
class_mape_results = {}
all_classes = {cls for counts in ground_truth.values() for cls in counts.keys()}

for cls in all_classes:
    actual_values = []
    predicted_values = []
    
    for video in ground_truth:
        if cls in ground_truth[video]:  # Só consideramos classes que aparecem no ground truth
            actual_values.append(ground_truth[video].get(cls, 0))
            predicted_values.append(model_predictions.get(video, {}).get(cls, 0))

    class_mape_results[cls] = calculate_mape(np.array(actual_values), np.array(predicted_values))

save_stats_to_file(mape_results, class_mape_results)

print("Processamento concluído para todos os vídeos.")

#source myenv/bin/activate 
#python test_track.py