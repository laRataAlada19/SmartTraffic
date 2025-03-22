import numpy as np
import cv2
from model import is_duplicate
import math
from config import vehicle_timestamps, direction_summary, average_speed_bike, average_speed_bus, average_speed_car, average_speed_motorcycle, average_speed_truck
from datetime import datetime
from collections import Counter

def _map_direction_(track, track_id):
    start_x, start_y = track[0]  # First recorded position
    end_x, end_y = track[-1]  # Last recorded position

    dx, dy = end_x - start_x, start_y - end_y  # Inverted Y-axis for correct orientation

    # Compute angle in degrees
    angle = math.degrees(math.atan2(dy, dx)) % 360

    # Map angle to direction
    if 337.5 <= angle < 360 or 0 <= angle < 22.5:
        direction = "E"
    elif 22.5 <= angle < 67.5:
        direction = "NE"
    elif 67.5 <= angle < 112.5:
        direction = "N"
    elif 112.5 <= angle < 157.5:
        direction = "NW"
    elif 157.5 <= angle < 202.5:
        direction = "W"
    elif 202.5 <= angle < 247.5:
        direction = "SW"
    elif 247.5 <= angle < 292.5:
        direction = "S"
    else:
        direction = "SE"

    # Store direction history
    if track_id not in direction_summary:
        direction_summary[track_id] = []  # Initialize list for each vehicle

    direction_summary[track_id].append(direction)  # Append new direction for this vehicle

def process_frame(frame, model, detected_vehicles, class_counter, track_history):
    results = model.track(frame, persist=True)
    
    if results and results[0].boxes and results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        conf_list = results[0].boxes.conf.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        annotated_frame = results[0].plot()

        vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bike'}
        for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
            x, y, w, h = box
            if model.names[int(cls)] in vehicle_classes and conf >= 0.6:
                if track_id not in detected_vehicles and not is_duplicate(detected_vehicles, box):
                    detected_vehicles[track_id] = box
                    class_name = model.names[int(cls)]
                    class_counter[class_name] += 1

            if track_id not in vehicle_timestamps:
                vehicle_timestamps[track_id] = {"timestamps": [], "positions": []}
                
            # Store the timestamp for this frame
            frame_timestamp = datetime.now()
            vehicle_timestamps[track_id]["timestamps"].append(frame_timestamp)
            vehicle_timestamps[track_id]["positions"].append((x, y))
            
            timestamps = vehicle_timestamps[track_id]["timestamps"]
            positions = vehicle_timestamps[track_id]["positions"]
            speed_kph = None
            
            if len(timestamps) >= 2:
                delta_t_list = []
                distance_list = []
                # Calculate time intervals (delta_t) and distances traveled between successive frames
                for i in range(1, len(timestamps)):
                    t1, t2 = timestamps[i - 1], timestamps[i]
                    delta_t = t2.timestamp() - t1.timestamp()
                    if delta_t > 0:
                        x1, y1 = positions[i - 1]
                        x2, y2 = positions[i]
                        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        delta_t_list.append(delta_t)
                        distance_list.append(distance)
                
                # Calculate speeds in meters per second (mps) for each frame and then average them
                speeds = [distance / delta_t for distance, delta_t in zip(distance_list, delta_t_list)]
                if len(speeds) > 0:
                    avg_speed_mps = sum(speeds) / len(speeds)
                    # Convert the average speed from meters per second (mps) to kilometers per hour (kph)
                    if avg_speed_mps is not None:
                        speed_kph = avg_speed_mps * 3.6
                        if model.names[int(cls)] == 'car':
                            average_speed_car.append(speed_kph)
                        elif model.names[int(cls)] == 'truck':
                            average_speed_truck.append(speed_kph)
                        elif model.names[int(cls)] == 'bus':
                            average_speed_bus.append(speed_kph)
                        elif model.names[int(cls)] == 'motorcycle':
                            average_speed_motorcycle.append(speed_kph)
                        elif model.names[int(cls)] == 'bike':
                            average_speed_bike.append(speed_kph)
                    else:
                        speed_kph = None
                else:
                    avg_speed_mps = None

            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            if len(track) > 5:  # Ensure we have enough data points for direction calculation'
                _map_direction_(track, track_id)
            
            # desenha a trajetoria do veiculo, ao usar o track_history para armazenar as coordenadas do centro da caixa 
            # delimitadora do veiculo em cada frame.
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

        return annotated_frame
    return frame
