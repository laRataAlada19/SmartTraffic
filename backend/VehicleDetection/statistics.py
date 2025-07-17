import cv2
import os

video_paths = [
    "/home/user/projeto_informatico/video_20250703-175423.mp4",
    "/home/user/projeto_informatico/video_20250710-103349.mp4",
    "/home/user/projeto_informatico/video_20250710-112403.mp4",
    "/home/user/projeto_informatico/video_20250710-125628.mp4",
    "/home/user/projeto_informatico/video_20250710-131730.mp4",
    "/home/user/projeto_informatico/3078508-hd_1920_1080_30fps.mp4",
    "/home/user/projeto_informatico/2431853-hd_1920_1080_25fps.mp4",
    "/home/user/projeto_informatico/2252223-uhd_3840_2160_30fps.mp4",
    "/home/user/projeto_informatico/2103099-uhd_3840_2160_30fps.mp4"
]
output_dir = "/home/user/projeto_informatico/backend/VehicleDetection/testing_dataset/imgs"
os.makedirs(output_dir, exist_ok=True)

for video_path in video_paths:
    cap = cv2.VideoCapture(video_path)
    frame_rate = 5  # Extract 1 frame every 5 frames

    i = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % frame_rate == 0:
            filename = os.path.join(output_dir, f"frame_{saved:05}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
        i += 1

    cap.release()
    print(f"Saved {saved} frames to {output_dir}")
