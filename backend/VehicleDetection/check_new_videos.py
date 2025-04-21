import os
import subprocess
from datetime import datetime

WATCH_DIRS = os.environ.get("WATCH_DIR", "/app/backend/VehicleDetection/videos/cam1").split(',')

SEEN_FILES_PATH = "/app/backend/VehicleDetection/data/seen_videos.txt"
MAIN_SCRIPT_PATH = "/app/backend/VehicleDetection/main.py"
LOG_PATH = (
    "/var/log/cron_VehicleDetection.log"
    if os.environ.get("DOCKER_ENV") == "true"
    else "/app/backend/VehicleDetection/logs/cron_VehicleDetection.log"
)

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}\n"
    print(full_message.strip())  # Still prints to stdout
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(full_message)

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
        log(f"New files detected: {len(new_files)}")
        try:
            result = subprocess.run(["/usr/local/bin/python3", MAIN_SCRIPT_PATH], check=True, capture_output=True, text=True)
            log("main.py executed successfully.")
            log("main.py output:\n" + result.stdout.strip())
            save_seen_files(current_files)
        except subprocess.CalledProcessError as e:
            log(f"Error running main.py: {e}")
            log(f"stderr:\n{e.stderr.strip()}")

    else:
        log("No new files detected.")

if __name__ == "__main__":
    main()