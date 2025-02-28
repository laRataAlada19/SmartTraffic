from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

model = YOLO('yolov8n.pt')  

#bmw_320I.MOV
#TestVideo.mp4

file_path = 'bmw_320I.MOV'
cap = cv2.VideoCapture(file_path)

class_counter = {}
aux = True
detected_vehicles = set() # para guardar cada veiculo detetado uma unica vez
track_history = defaultdict(lambda: [])

while aux:
    aux, frame = cap.read()  # Se cap.read não tiver mais frames para ler, aux será False
    if aux:
        results = model.track(frame, persist=True)  # persist=True para manter o tracking
        
        if results is not None and results[0] is not None and results[0].boxes is not None and results[0].boxes.id is not None:
            
            boxes = results[0].boxes.xywh.cpu() # caixa delimitadora (x, y, w, h)
            conf_list = results[0].boxes.conf.cpu() # mostra a acuracy da detecção
            track_ids = results[0].boxes.id.int().cpu().tolist() # ID do objeto
            clss = results[0].boxes.cls.cpu().tolist() # classe do objeto
            annotated_frame = results[0].plot() # desenha as boxes ao redor dos objetos

            # Contagem para cada classe
            for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
                x, y, w, h = box # coordenadas da caixa delimitadora
                class_id = int(cls) # ID da classe

                if track_id not in detected_vehicles: # se o objeto não estiver na lista de tracking, ent adicionar
                    detected_vehicles.add(track_id) # adicionar o objeto à lista de objetos detetados
                    class_name = model.names[class_id]
                    class_counter[class_name] = class_counter.get(class_name, 0) + 1# incrementar a contagem de classes
                
                track = track_history[track_id] # obter o histórico de tracking do objeto
                
                track.append((float(x), float(y))) # adicionar a posição atual do objeto ao histórico de tracking
                if len(track) > 30: # para nao guardar muitos frames
                    track.pop(0)
                    
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2)) # combinar todos os pontos de tracking
                cv2.polylines(annotated_frame, [points], isClosed=False, color = (0, 255, 0) , thickness=2) # desenhar a linha de tracking
        
        cv2.imshow('Frame', annotated_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Exibir contagem de classes
for class_name, count in class_counter.items():
    print(f"Classe: {class_name}, Contagem: {count}")

#source myenv/bin/activate 
#python teste_nk.py