from ultralytics import YOLO
import numpy as np

def load_model():
    return YOLO('yolov8n.pt')

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

    return inter_area / (box1_area + box2_area - inter_area + 1e-6)

def is_duplicate(detected_vehicles, new_box):
    for old_box in detected_vehicles.values():
        if compute_iou(old_box, new_box) > 0.5:
            return True
    return False
