import numpy as np
import cv2
from collections import deque, defaultdict
from model import is_duplicate

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
            if model.names[int(cls)] in vehicle_classes and conf >= 0.6:
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
