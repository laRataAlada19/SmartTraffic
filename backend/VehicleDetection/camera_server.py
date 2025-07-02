from flask import Flask, request, jsonify
import subprocess
import re
from flask_cors import CORS
from threading import Thread, Event
import os
import motion_recorder

app = Flask(__name__)

global rec 
rec = None

CORS(app, resources={r"/*": {"origins": "*"}})

processes = {}




@app.route('/cameras', methods=['GET'])
def listar_cameras_ffmpeg():
    try:
        result = subprocess.run(
            ['ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        output = result.stderr
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    cameras = []
    for line in output.splitlines():
        m = re.search(r'\[(\d+)\] (.+)', line)
        if m:
            index = int(m.group(1))
            name = m.group(2).strip()
            cameras.append({'index': index, 'name': name})

    return jsonify(cameras)

@app.route("/start", methods=["POST"])
def start_recording():
    global rec  

    data = request.json
    name = data['camera_name']
    location_id = str(data['location_id'])

    if rec is not None:
        return jsonify({'error': 'Gravação já está em andamento'}), 407

    camera_map = motion_recorder.ler_mapeamento()
    index = camera_map.get(name)

    if index is None:
        return jsonify({'error': f'Câmara "{name}" não encontrada no mapeamento.'}), 404

    base_dir = os.path.join(os.path.dirname(__file__), "videos")
    output_dir = os.path.join(base_dir, location_id)
    os.makedirs(output_dir, exist_ok=True)

    stop_event = Event()  
    t = Thread(target=motion_recorder.detect_motion_and_record, args=(index, output_dir, stop_event))
    rec = location_id  
    t.start()
    processes[location_id] = {'thread': t, 'stop_event': stop_event}  

    return jsonify({'message': 'Gravação iniciada'})

@app.route("/status", methods=["GET"])
def get_status():
    global rec  
    if rec is not None:
        return jsonify({'status': 'Gravação em andamento', 'location_id': rec}),200
    else:
        return jsonify({'status': 'Nenhuma gravação em andamento'}), 202

@app.route("/stop", methods=["POST"])
def stop_recording():
    global rec  
    location_id = str(request.json['location_id'])
    if location_id in processes:
        process_info = processes[location_id]
        stop_event = process_info['stop_event']
        thread = process_info['thread']

        stop_event.set()  
        thread.join(timeout=1)  
        del processes[location_id]
        rec = None
   
        return jsonify({'message': 'Gravação parada'})
    else:
        return jsonify({'error': 'Nenhum processo encontrado para esta localização'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
