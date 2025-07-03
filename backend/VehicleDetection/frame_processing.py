import numpy as np
import cv2
from model import is_duplicate
import math
from config import vehicle_timestamps, direction_summary, average_speed_bike, average_speed_bus, average_speed_car, average_speed_motorcycle, average_speed_truck
from datetime import datetime
from collections import Counter


def process_frame(frame, model, detected_vehicles, class_counter, track_history, speed_limited_of_street, speed_violations):
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

            vehicle_timestamps[track_id]["timestamps"].append(datetime.now())
            vehicle_timestamps[track_id]["positions"].append((x, y))


            if len(vehicle_timestamps[track_id]["timestamps"]) >= 2:
                t1, t2 = vehicle_timestamps[track_id]["timestamps"][-2:]
                p1, p2 = vehicle_timestamps[track_id]["positions"][-2:]

                distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

              
                time_diff = (t2 - t1).total_seconds()

                if time_diff > 0:
                    speed = distance / time_diff  

                    if speed > speed_limited_of_street:
                        speed_violations += 1

            if track_id not in track_history:
                track_history[track_id] = []
            track = track_history[track_id]
            track.append((float(box[0]), float(box[1])))
            # delimitadora do veiculo em cada frame.
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 0), thickness=2)


        return annotated_frame, track_history  # Return track_history along with the annotated frame
    
    print("No boxes detected or no IDs assigned.")
    return frame,track_history