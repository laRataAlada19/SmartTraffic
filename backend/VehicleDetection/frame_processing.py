import numpy as np
import cv2
from model import is_duplicate
import math
from config import vehicle_timestamps, direction_summary, average_speed_bike, average_speed_bus, average_speed_car, average_speed_motorcycle, average_speed_truck, average_speed_all
from datetime import datetime
from collections import defaultdict
from filterpy.kalman import KalmanFilter

# Configurações de calibração (AJUSTE ESTES VALORES CONFORME SUA CENA)
PIXELS_PER_METER = 10  # 10 pixels = 1 metro (calibre com um objeto de tamanho conhecido)
MIN_FRAMES_FOR_SPEED = 5  # Mínimo de frames para cálculo de velocidade
SPEED_SMOOTHING_WINDOW = 5  # Janela para suavização de velocidade
MIN_TIME_DIFF = 0.1  # 100ms (ignorar intervalos menores que isso)

def create_kalman_filter():
    """Cria e configura um filtro de Kalman para suavização de posições"""
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.F = np.array([[1, 0, 1, 0],   # Matriz de transição de estado
                    [0, 1, 0, 1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    kf.H = np.array([[1, 0, 0, 0],   # Matriz de observação
                    [0, 1, 0, 0]])
    kf.P *= 1000                     # Matriz de covariância
    kf.R = 5                         # Ruído de medição
    kf.Q = 0.1                       # Ruído do processo
    return kf

def pixels_to_meters(pixel_distance):
    """Converte distância em pixels para metros"""
    return pixel_distance / PIXELS_PER_METER

def calculate_speed(positions, timestamps, fps):
    """Calcula velocidade com base nas posições e tempos"""
    if len(positions) < 2:
        return None
    
    # Calcula usando o FPS como base para intervalos consistentes
    total_frames = len(positions)
    total_time = total_frames / fps
    if total_time <= 0:
        return None
    
    # Calcula distância total percorrida
    total_distance_pixels = 0
    for i in range(1, len(positions)):
        x1, y1 = positions[i-1]
        x2, y2 = positions[i]
        total_distance_pixels += math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    total_distance_meters = pixels_to_meters(total_distance_pixels)
    speed_mps = total_distance_meters / total_time
    speed_kph = speed_mps * 3.6
    
    return speed_kph

def process_frame(frame, model, detected_vehicles, class_counter, track_history, speed_limited_of_street, speed_violations, fps):
    results = model.track(frame, persist=True)
    
    if results and results[0].boxes and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        conf_list = results[0].boxes.conf.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        # Dicionário para armazenar filtros de Kalman
        if not hasattr(process_frame, 'kalman_filters'):
            process_frame.kalman_filters = defaultdict(create_kalman_filter)

        vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bike'}
        
        for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
            x, y, w, h = box
            
            # Suavização com filtro de Kalman
            kf = process_frame.kalman_filters[track_id]
            kf.predict()
            kf.update(np.array([x, y]))
            smoothed_x, smoothed_y = kf.x[0], kf.x[1]
            
            if model.names[int(cls)] in vehicle_classes and conf >= 0.6:
                if track_id not in detected_vehicles and not is_duplicate(detected_vehicles, box):
                    detected_vehicles[track_id] = box
                    class_name = model.names[int(cls)]
                    class_counter[class_name] += 1

            # Armazenamento de histórico com posições suavizadas
            if track_id not in vehicle_timestamps:
                vehicle_timestamps[track_id] = {"timestamps": [], "positions": []}
            
            frame_timestamp = datetime.now()
            vehicle_timestamps[track_id]["timestamps"].append(frame_timestamp)
            vehicle_timestamps[track_id]["positions"].append((smoothed_x, smoothed_y))
            
            timestamps = vehicle_timestamps[track_id]["timestamps"]
            positions = vehicle_timestamps[track_id]["positions"]
            
            # Cálculo de velocidade apenas com dados suficientes
            if (len(timestamps) >= MIN_FRAMES_FOR_SPEED and track_id in detected_vehicles 
                and not is_duplicate(detected_vehicles, box) and track_id not in speed_violations):
                
                speed_kph = calculate_speed(positions, timestamps, fps)
                
                if speed_kph is not None:
                    class_name = model.names[int(cls)]
                    
                    # Verificar violação de velocidade
                    if speed_kph > speed_limited_of_street:
                        speed_violations[track_id] = speed_kph
                        print(f"Violacao de velocidade detectada para ID {track_id}: {speed_kph:.2f} km/h")
                    
                    # Armazenar velocidade por classe
                    if class_name == 'car':
                        average_speed_car.append(speed_kph)
                    elif class_name == 'truck':
                        average_speed_truck.append(speed_kph)
                    elif class_name == 'bus':
                        average_speed_bus.append(speed_kph)
                    elif class_name == 'motorcycle':
                        average_speed_motorcycle.append(speed_kph)
                    elif class_name == 'bike':
                        average_speed_bike.append(speed_kph)
                    
                    # Atualizar média geral
                    all_speeds = average_speed_car + average_speed_truck + average_speed_bus + average_speed_motorcycle + average_speed_bike
                    if all_speeds:
                        avg_all = sum(all_speeds) / len(all_speeds)
                        print(f"Velocidade média de todos os veículos: {avg_all:.2f} km/h")
            
            # Atualizar histórico de rastreamento
            if track_id not in track_history:
                track_history[track_id] = []
            track_history[track_id].append((smoothed_x, smoothed_y))
            
            # Desenhar trajeto
            points = np.array(track_history[track_id], np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame, track_history, speed_violations
    
    return frame, track_history, speed_violations