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

def arredondar_para_proximo_5_minutos(data_hora):
    data_hora = data_hora.replace(second=0, microsecond=0)
    minutos_extra = (5 - data_hora.minute % 5) % 5
    return data_hora + timedelta(minutes=minutos_extra)

def process_video(video_file, model, ground_truth, total_class_counter, time_of_start, camera):
    db = Database()
    print(f"Processing: {video_file}")
    
    if not os.path.exists(video_file):
        print(f"O arquivo {video_file} não foi encontrado.")
        return

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Erro ao abrir {video_file}")
        return

    # Dados iniciais
    fps_video = cap.get(cv2.CAP_PROP_FPS)
    frame_number = 0
    track_history = {}
    ultimo_tempo_guardado = arredondar_para_proximo_5_minutos(time_of_start)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Tempo atual do vídeo com base no número de frames
        current_video_time = time_of_start + timedelta(seconds=(frame_number / fps_video))
        tempo_agrupado = arredondar_para_proximo_5_minutos(current_video_time)

        frame = cv2.resize(frame, (640, 480))
        frame, track_history = process_frame(frame, model, detected_vehicles, class_counter, track_history, camera)

        # Mostra o FPS 
        cv2.putText(frame, f"Frame: {frame_number}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)

        
        if tempo_agrupado != ultimo_tempo_guardado:
            print(f"[{tempo_agrupado}] Salvando dados na base de dados...")
            if not db.exists_result(tempo_agrupado, camera):
                #db.save_results_to_bd(class_counter, total_class_counter, tempo_agrupado, camera)
                print(f"[{tempo_agrupado}] Dados salvos na base de dados.")
            else:
                print(f"[{tempo_agrupado}] Já existe entrada para esta câmara. Ignorado.")
            ultimo_tempo_guardado = tempo_agrupado

        frame_number += 1
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break



    for track_id in track_history:
        _map_direction_(track_history, track_id, camera)
    if not db.exists_result(ultimo_tempo_guardado, camera):
        print(f"[{ultimo_tempo_guardado}] Salvando dados finais na base de dados (forçado no fim do vídeo)...")
        db.save_results_to_bd(class_counter, total_class_counter, ultimo_tempo_guardado, camera)
    else:
        print(f"[{ultimo_tempo_guardado}] Dados já existentes no fim do vídeo.")
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
        query = "SELECT direction FROM location WHERE location_id = 8"
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

def _map_direction_(track_history, track_id, camera):
    # Ensure the track exists and is not empty
    if track_id not in track_history or not track_history[track_id]:
        print(f"Track ID {track_id} is missing or empty. Skipping direction mapping.")
        return

    # Ensure the track_id is in detected_vehicles
    if track_id not in detected_vehicles:
        print(f"Track ID {track_id} is not in detected_vehicles. Skipping direction mapping.")
        return

    track = track_history[track_id]
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

    if camera_direction == "N":
        if 22.5 <= angle < 67.5:
            direction = "NE"
        elif 67.5 <= angle < 112.5:
            direction = "N"
        elif 112.5 <= angle < 157.5:
            direction = "NW"
        elif 157.5 <= angle < 202.5:
            direction = "W"
        elif 202.5 <= angle < 247.5:
            direction = "SW"
        elif 247.5 <= angle < 292.5:
            direction = "S"
        elif 292.5 <= angle < 337.5:
            direction = "SE"
        else:
            direction = "E"
    elif camera_direction == "S":
        if 22.5 <= angle < 67.5:
            direction = "SW"
        elif 67.5 <= angle < 112.5:
            direction = "S"
        elif 112.5 <= angle < 157.5:
            direction = "SE"
        elif 157.5 <= angle < 202.5:
            direction = "E"
        elif 202.5 <= angle < 247.5:
            direction = "NE"
        elif 247.5 <= angle < 292.5:
            direction = "N"
        elif 292.5 <= angle < 337.5:
            direction = "NW"
        else:
            direction = "W"
    elif camera_direction == "E":
        if 22.5 <= angle < 67.5:
            direction = "SE"
        elif 67.5 <= angle < 112.5:
            direction = "E"
        elif 112.5 <= angle < 157.5:
            direction = "NE"
        elif 157.5 <= angle < 202.5:
            direction = "N"
        elif 202.5 <= angle < 247.5:
            direction = "NW"
        elif 247.5 <= angle < 292.5:
            direction = "W"
        elif 292.5 <= angle < 337.5:
            direction = "SW"
        else:
            direction = "S"
    elif camera_direction == "W":
        if 22.5 <= angle < 67.5:
            direction = "NW"
        elif 67.5 <= angle < 112.5:
            direction = "W"
        elif 112.5 <= angle < 157.5:
            direction = "SW"
        elif 157.5 <= angle < 202.5:
            direction = "S"
        elif 202.5 <= angle < 247.5:
            direction = "SE"
        elif 247.5 <= angle < 292.5:
            direction = "E"
        elif 292.5 <= angle < 337.5:
            direction = "NE"
        else:
            direction = "N"
    else:
        print(f"Direção da câmera '{camera}' não reconhecida. Usando cálculo padrão.")
        if 22.5 <= angle < 67.5:
            direction = "NE"
        elif 67.5 <= angle < 112.5:
            direction = "N"
        elif 112.5 <= angle < 157.5:
            direction = "NW"
        elif 157.5 <= angle < 202.5:
            direction = "W"
        elif 202.5 <= angle < 247.5:
            direction = "SW"
        elif 247.5 <= angle < 292.5:
            direction = "S"
        elif 292.5 <= angle < 337.5:
            direction = "SE"
        else:
            direction = "E"

    # Store direction history
    direction_summary[track_id] = direction