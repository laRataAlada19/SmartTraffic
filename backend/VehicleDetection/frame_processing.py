import numpy as np
import cv2
from model import is_duplicate
import math
from config import vehicle_timestamps, direction_summary, average_speed_bike, average_speed_bus, average_speed_car, average_speed_motorcycle, average_speed_truck
from datetime import datetime
from collections import Counter


def process_frame(frame, model, detected_vehicles, class_counter, track_history,camera):
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
            if track_id not in track_history:
                track_history[track_id] = []
            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            # delimitadora do veiculo em cada frame.
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)

 
        return annotated_frame, track_history  # Return track_history along with the annotated frame
    
    return frame
