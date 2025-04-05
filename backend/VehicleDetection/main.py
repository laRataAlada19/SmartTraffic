from config import video_files, ground_truth,total_class_counter,camera
from model import load_model
from video_processing import process_video
from file_operations import clean_file
from datetime import datetime

def main():
    model = load_model()
    clean_file("results.txt")

   
    time_of_start = datetime.strptime("2025-03-20 16:35:40", "%Y-%m-%d %H:%M:%S")
    for video in video_files:
        print(f"Processing: {video}")
        process_video(video, model, ground_truth, total_class_counter,time_of_start,camera)

if __name__ == "__main__":
    main()

#source myenv/bin/activate 