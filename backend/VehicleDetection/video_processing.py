import cv2
from frame_processing import process_frame
from file_operations import save_results_to_file
from database import Database
from datetime import timedelta, datetime
import math
import os
from config import detected_vehicles, class_counter, track_history, direction_summary, total_class_counter

db = Database()

def arredondar_para_proximo_5_minutos(data_hora):
    data_hora = data_hora.replace(second=0, microsecond=0)
    minutos_extra = (5 - data_hora.minute % 5) % 5
    return data_hora + timedelta(minutes=minutos_extra)

def _map_direction_(track_history, track_id, location, id):
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
    location_direction = db.get_location_direction(id)
    if location_direction:
        print(f"Direção da câmera '{location}': {location_direction}")
    else:
        print(f"Usando cálculo padrão, pois a direção da câmera '{location}' não foi encontrada.")

    # Map angle to direction

    if location_direction == "N" or location_direction == "NORTE" or location_direction == "NORTH":
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
    elif location_direction == "S" or location_direction == "SUL" or location_direction == "SOUTH":
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
    elif location_direction == "E" or location_direction == "LESTE" or location_direction == "EAST":
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
    elif location_direction == "W" or location_direction == "OESTE" or location_direction == "WEST":
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
    elif location_direction == "NE" or location_direction == "NORDESTE" or location_direction == "NORTHEAST":
        if 22.5 <= angle < 67.5:
            direction = "N"
        elif 67.5 <= angle < 112.5:
            direction = "NE"
        elif 112.5 <= angle < 157.5:
            direction = "E"
        elif 157.5 <= angle < 202.5:
            direction = "SE"
        elif 202.5 <= angle < 247.5:
            direction = "S"
        elif 247.5 <= angle < 292.5:
            direction = "SW"
        elif 292.5 <= angle < 337.5:
            direction = "W"
        else:
            direction = "NW"
    elif location_direction == "NW" or location_direction == "NOROESTE" or location_direction == "NORTHWEST":
        if 22.5 <= angle < 67.5:
            direction = "W"
        elif 67.5 <= angle < 112.5:
            direction = "NW"
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
    elif location_direction == "SE" or location_direction == "SUDESTE" or location_direction == "SOUTHEAST":
        if 22.5 <= angle < 67.5:
            direction = "E"
        elif 67.5 <= angle < 112.5:
            direction = "SE"
        elif 112.5 <= angle < 157.5:
            direction = "S"
        elif 157.5 <= angle < 202.5:
            direction = "SW"
        elif 202.5 <= angle < 247.5:
            direction = "W"
        elif 247.5 <= angle < 292.5:
            direction = "NW"
        elif 292.5 <= angle < 337.5:
            direction = "N"
        else:
            direction = "NE"
    elif location_direction == "SW" or location_direction == "SUDOESTE" or location_direction == "SOUTHWEST":
        if 22.5 <= angle < 67.5:
            direction = "S"
        elif 67.5 <= angle < 112.5:
            direction = "SW"
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
    else:
        print(f"Direção da câmera '{location}' não reconhecida. Usando cálculo padrão.")
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

def process_video(video_file, model, total_class_counter, time_of_start, location):
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
        frame, track_history = process_frame(frame, model, detected_vehicles, class_counter, track_history)

        # Mostra o FPS 
        #cv2.putText(frame, f"Frame: {frame_number}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        #cv2.imshow('Frame', frame)

        id = db.get_id(location)

        if tempo_agrupado != ultimo_tempo_guardado:
            print("Salvando dados na base de dados...")
            if id is None:
                print(f"Erro ao obter o ID da localização '{location}'. Verifique se a câmera está registrada no banco de dados.")
                return
            if not db.exists_result(tempo_agrupado, id):
                db.save_results_to_bd(class_counter, total_class_counter, tempo_agrupado, location, id)
                print("Dados salvos na base de dados.")
            else:
                print("Já existe entrada para esta câmara. Ignorado.")
            ultimo_tempo_guardado = tempo_agrupado

        frame_number += 1
        #if cv2.waitKey(25) & 0xFF == ord('q'):
            #break

    for track_id in track_history:
        _map_direction_(track_history, track_id, location, id)
    if not db.exists_result(ultimo_tempo_guardado, id):
        print("Salvando dados finais na base de dados (forçado no fim do vídeo)...")
        db.save_results_to_bd(class_counter, total_class_counter, ultimo_tempo_guardado, location, id)
    else:
        print("Dados já existentes no fim do vídeo.")
    cap.release()
    #cv2.destroyAllWindows()
    save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter)
