from collections import defaultdict, deque, Counter
import os

DB_CONFIG_neon_tech = {
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_o1YqvCrGuK5O",
    "port": "5432",
    "host": "ep-damp-sunset-a2kojsnk-pooler.eu-central-1.aws.neon.tech"
}

DATABASE_SCHEMA = "vehicle_detection"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
videos_directory = os.path.join(BASE_DIR, "videos")

total_class_counter = defaultdict(int)

class_counter = defaultdict(int)

detected_vehicles = {}

track_history = defaultdict(lambda: deque(maxlen=30))

vehicle_timestamps = defaultdict(list)

direction_summary = defaultdict(Counter)

average_speed_car = []
average_speed_truck = []
average_speed_bus = []
average_speed_motorcycle = []
average_speed_bike = []
average_speed_all = 0

average_speeds_summary = {"car": average_speed_car, "truck": average_speed_truck, "bus": average_speed_bus, "motorcycle": average_speed_motorcycle, "bike": average_speed_bike}