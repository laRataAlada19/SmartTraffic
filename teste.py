from ultralytics import YOLO

model = YOLO('yolov8n.pt')  
model.predict('TestVideo.mp4', show=True)
#pequeno teste para verificar se o modelo está funcionar corretamente