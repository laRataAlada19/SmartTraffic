import cv2
import time
from frame_processing import process_frame
from file_operations import save_results_to_file
from database import Database
from datetime import datetime, timedelta
import os
from config import detected_vehicles, class_counter, track_history

def process_video(video_file, model, ground_truth, total_class_counter,time_of_start):
    db = Database()
    print(f"Processing: {video_file}")
    if os.path.exists(video_file):
        print(f"O arquivo {video_file} existe.")
    else:
        print(f"O arquivo {video_file} não foi encontrado.")
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Erro ao abrir {video_file}")
        return
    
    prev_time = time.time()

    current_time = time_of_start
    next_save_time = current_time + timedelta(minutes=1)  # Próximo minuto para salvar os dados

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        frame = process_frame(frame, model, detected_vehicles, class_counter, track_history)

        curr_time = time.time()
        fps = 1 / max(curr_time - prev_time, 1e-6)
        prev_time = curr_time
        
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
       
        if datetime.now() >= next_save_time:
            print(f"Salvando dados na base de dados para o minuto: {next_save_time}")
            db.save_results_to_bd(video_file, detected_vehicles, class_counter, total_class_counter)
            next_save_time += timedelta(minutes=1) 

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    #db.save_results_to_bd(video_file, detected_vehicles, class_counter, total_class_counter)
    save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter)
