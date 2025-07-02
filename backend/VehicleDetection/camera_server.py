from flask import Flask, jsonify
import subprocess
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite pedidos do Vue (localhost:5173, etc.)

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

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
