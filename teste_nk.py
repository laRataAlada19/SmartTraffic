from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

#Iniciar o modelo
model = YOLO('yolov8n.pt')  

#bmw_320I.MOV
#TestVideo.mp4

# Abrir o ficheiro de vídeo
file_path = 'Small.mp4'
cap = cv2.VideoCapture(file_path)

#Inicializaçao de variaveis
class_counter = defaultdict(int)
aux = True
detected_vehicles = set() 
track_history = defaultdict(lambda: [])
total_detections_wanted = 0
class_relevant = {'car', 'truck', 'bus', 'moto', 'bike'}

# Loop para ler os frames do vídeo
while aux:
    aux, frame = cap.read()  # Se cap.read não tiver mais frames para ler, aux será False
    if aux:
        results = model.track(frame, persist=True)  # Tracking do modelo YOLO  
        if results is not None and results[0] is not None and results[0].boxes is not None and results[0].boxes.id is not None: # se houver objetos detetados
            
            boxes = results[0].boxes.xywh.cpu() #Caixas do video
            conf_list = results[0].boxes.conf.cpu() #Mostra a acuracy da detecção na caixa
            track_ids = results[0].boxes.id.int().cpu().tolist() # ID do objeto
            clss = results[0].boxes.cls.cpu().tolist() #Classe do objeto
            annotated_frame = results[0].plot() #Desenha as boxes ao redor dos objetos

            # Contagem para cada classe
            for box, track_id, cls, conf in zip(boxes, track_ids, clss, conf_list):
                x, y, w, h = box #Coordenadas da caixa delimitadora
                class_id = int(cls) # ID da classe

                if track_id not in detected_vehicles: # Se o objeto não estiver na lista de tracking, ent adicionar
                    detected_vehicles.add(track_id) # Adicionar o objeto à lista de objetos detetados
                    class_name = model.names[int(class_id)] # Obter o nome da classe
                    class_counter[class_name] +=1 # Incrementar o contador da classe

                track = track_history[track_id] # obter o histórico de tracking do objeto
                
                track.append((float(x), float(y))) # adicionar a posição atual do objeto ao histórico de tracking
                if len(track) > 30: # para nao guardar muitos frames
                    track.pop(0)
                    
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2)) # combinar todos os pontos de tracking
                cv2.polylines(annotated_frame, [points], isClosed=False, color = (0, 255, 0) , thickness=2) # desenhar a linha de tracking
        
        cv2.imshow('Frame', annotated_frame)# Mostrar o frame com as caixas desenhadas
        if cv2.waitKey(25) & 0xFF == ord('q'):# Se a tecla 'q' for pressionada, sair do loop
            break

# Se o vídeo acabar, sair do loop
cap.release()
cv2.destroyAllWindows()


# Imprimir resultados   
print(f"Total Detection: {len(detected_vehicles)}")

for class_name, count in class_counter.items():
    if class_name in class_relevant:
        print(f"Classe: {class_name}, Contagem: {count}")
        total_detections_wanted += count

print(f"Total Detections Wanted: {total_detections_wanted}")
#source myenv/bin/activate 
#python teste_nk.py