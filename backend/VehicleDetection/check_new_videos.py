import os
import subprocess
from datetime import datetime

WATCH_DIRS = [
    "./backend/VehicleDetection/videos/cam1",
]

SEEN_FILES_PATH = "./backend/VehicleDetection/data/seen_videos.txt"
MAIN_SCRIPT_PATH = "./backend/VehicleDetection/main.py"

def load_seen_files():
    if not os.path.exists(SEEN_FILES_PATH):
        return set()
    with open(SEEN_FILES_PATH, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_seen_files(files):
    os.makedirs(os.path.dirname(SEEN_FILES_PATH), exist_ok=True)
    with open(SEEN_FILES_PATH, "w") as f:
        for file in sorted(files):
            f.write(file + "\n")

def main():
    seen_files = load_seen_files()

    current_files = set()

    for folder in WATCH_DIRS:
        for root, _, files in os.walk(folder):
            for name in files:
                if name.endswith((".mp4", ".avi")):
                    full_path = os.path.join(root, name)
                    current_files.add(full_path)

    new_files = current_files - seen_files

    if new_files:
        print(f"New files detected: {len(new_files)}")
        try:
            result = subprocess.run(["python", MAIN_SCRIPT_PATH], check=True, capture_output=True, text=True)
            print("main.py output:\n", result.stdout)
            save_seen_files(current_files)
        except subprocess.CalledProcessError as e:
            print(f"Error running main.py: {e}\n{e.stderr}")


if __name__ == "__main__":
    main()
