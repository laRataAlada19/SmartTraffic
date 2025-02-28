from ultralytics import YOLO

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
