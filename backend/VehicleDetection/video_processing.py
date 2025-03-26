import cv2
import time
from frame_processing import process_frame
from file_operations import save_results_to_file
from database import Database
from datetime import datetime, timedelta
import math
import psycopg2
import os
from config import detected_vehicles, class_counter, track_history, direction_summary, total_class_counter, DB_CONFIG

def process_video(video_file, model, ground_truth, total_class_counter,time_of_start,camera):
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
        frame = process_frame(frame, model, detected_vehicles, class_counter, track_history,camera)

        curr_time = time.time()
        fps = 1 / max(curr_time - prev_time, 1e-6)
        prev_time = curr_time
        
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
       
        if datetime.now() >= next_save_time:
            print(f"Salvando dados na base de dados para o minuto: {next_save_time}")
            db.save_results_to_bd(video_file, detected_vehicles, class_counter, total_class_counter,camera)
            next_save_time += timedelta(minutes=1) 

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    for track_id in track_history:
        _map_direction_(track_history, track_id, camera)
    cap.release()
    cv2.destroyAllWindows()
    save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter)

def get_camera_direction(camera_name):
    """
    Conecta ao banco de dados e retorna a direção da câmera com base no nome.
    """
    try:
        # Conectar ao banco de dados
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Query para buscar a direção da câmera
        query = "SELECT direction FROM camera WHERE name = %s"
        cursor.execute(query, (camera_name,))
        result = cursor.fetchone()

        # Fechar a conexão
        cursor.close()
        connection.close()

        # Retornar a direção, se encontrada
        if result:
            return result[0]  # A direção está no primeiro índice do resultado
        else:
            print(f"Nenhuma câmera encontrada com o nome: {camera_name}")
            return None
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados ou executar a query: {e}")
        return None

def _map_direction_(track, track_id, camera):
    start_x, start_y = track[0]  # First recorded position
    end_x, end_y = track[-1]  # Last recorded position

    dx, dy = end_x - start_x, start_y - end_y  # Inverted Y-axis for correct orientation

    if abs(dx) < 5 and abs(dy) < 5:
        return None
    # Compute angle in degrees
    angle = math.degrees(math.atan2(dy, dx)) % 360

    # Buscar a direção da câmera no banco de dados
    camera_direction = get_camera_direction(camera)
    if camera_direction:
        print(f"Direção da câmera '{camera}': {camera_direction}")
    else:
        print(f"Usando cálculo padrão, pois a direção da câmera '{camera}' não foi encontrada.")

    # Map angle to direction

    if camera_direction == "norte":
        if 45 <= angle < 135:
            direction = "N"
        elif 135 <= angle < 225:
            direction = "W"
        elif 225 <= angle < 315:
            direction = "S"
        else:
            direction = "E"
    elif camera_direction == "S":
        if 45 <= angle < 135:
            direction = "S"
        elif 135 <= angle < 225:
            direction = "E"
        elif 225 <= angle < 315:
            direction = "N"
        else:
            direction = "W"
    elif camera_direction == "E":
        if 45 <= angle < 135:
            direction = "E"
        elif 135 <= angle < 225:
            direction = "N"
        elif 225 <= angle < 315:
            direction = "W"
        else:
            direction = "S"
    elif camera_direction == "W":
        if 45 <= angle < 135:
            direction = "W"
        elif 135 <= angle < 225:
            direction = "S"
        elif 225 <= angle < 315:
            direction = "E"
        else:
            direction = "N"
    else:
        print(f"Direção da câmera '{camera}' não reconhecida. Usando cálculo padrão.")
        if 45 <= angle < 135:
            direction = "N"
        elif 135 <= angle < 225:
            direction = "W"
        elif 225 <= angle < 315:
            direction = "S"
        else:
            direction = "E"

    # Store direction history
    direction_summary[track_id] = direction