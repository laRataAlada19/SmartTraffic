from collections import defaultdict, deque, Counter
import psycopg2
import os


DB_CONFIG = {
    "dbname": "vehicle_detection",
    "user": "user",
    "password": "123",
    "port": "5432",
    "host": "host.docker.internal"
} #"port": "5433",

#videos_directory = "./backend/VehicleDetection/videos"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
videos_directory = os.path.join(BASE_DIR, "videos")

video_files_by_camera={}

for camera_folder in os.listdir(videos_directory):
    camera_path = os.path.join(videos_directory, camera_folder)
    if os.path.isdir(camera_path):
        video_files = [
            os.path.join(camera_path, file)
            for file in os.listdir(camera_path)
            if file.endswith(".mp4")
        ]
        video_files_by_camera[camera_folder] = video_files

for camera, videos in video_files_by_camera.items():
    print(f"Câmera: {camera}")
    for video in videos:
        print(f"  - {video}")

total_class_counter = defaultdict(int)

class_counter = defaultdict(int)

detected_vehicles = {}

track_history = defaultdict(lambda: deque(maxlen=30))

ground_truth = {
    "1.mp4": {"car": 37, "motorcycle": 1},
    "2.mp4": {"car": 205, "truck": 27, "motorcycle": 3},
    "3.mp4": {"car": 11, "motorcycle": 4, "bike": 2, "truck": 3},            
    "4.mp4": {"car": 59, "motorcycle": 68, "truck": 3},
    "5.mp4": {"car": 33, "bus": 1, "truck": 1}
}

vehicle_timestamps = defaultdict(list)

direction_summary = defaultdict(Counter)

average_speed_car = []
average_speed_truck = []
average_speed_bus = []
average_speed_motorcycle = []
average_speed_bike = []

average_speeds_summary = {"car": average_speed_car, "truck": average_speed_truck, "bus": average_speed_bus, "motorcycle": average_speed_motorcycle, "bike": average_speed_bike}