import json
import math
import cv2
import base64
from collections import defaultdict
from ultralytics import YOLO
import numpy as np
from ultralytics.utils.plotting import colors
from VehicleDetectionTracker.color_classifier.classifier import Classifier as ColorClassifier
from VehicleDetectionTracker.model_classifier.classifier import Classifier as ModelClassifier
from datetime import datetime

model_path="yolov8n.pt"


model = YOLO('yolov8n.pt')  
results=model.predict('TestVideo.mp4', show=True)
#pequeno teste para verificar se o modelo está funcionar corretamente

#codigo para guardar classes
class_counter={}

for result in results:
    for class_id in result.boxes.cls:
        class_name= model.names[int(class_id)]
        if class_name in class_counter:
            class_counter[class_name] += 1
        else:
            class_counter[class_name] = 1

for class_name, count in class_counter.items():
    print(f"Classe: {class_name}, Contagem: {count}")
