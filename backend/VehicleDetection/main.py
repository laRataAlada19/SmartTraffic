from config import total_class_counter, videos_directory
from model import load_model
from video_processing import process_video
from file_operations import clean_file
from datetime import datetime
import os

def get_video_files():
    video_files_by_location={}
    for location_folder in os.listdir(videos_directory):
        location_path = os.path.join(videos_directory, location_folder)
        if os.path.isdir(location_path):
            video_files = [
                os.path.join(location_path, file)
                for file in os.listdir(location_path)
                if file.endswith(".mp4")
            ]
            video_files_by_location[location_folder] = video_files

    for location, videos in video_files_by_location.items():
        print(f"Câmera: {location}")
        for video in videos:
            print(f"  - {video}")

    return video_files_by_location

def extract_timestamp(video_name):
    video_name = os.path.splitext(video_name)[0]  # Remove ".mp4"
    timestamp_str = video_name.split('_')[1]  # Get the part after "video_" YYYYMMDD-HHMMSS
    timestamp_str = f"{timestamp_str[:4]}-{timestamp_str[4:6]}-{timestamp_str[6:8]} {timestamp_str[9:11]}:{timestamp_str[11:13]}:{timestamp_str[13:]}" # format to "YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")  # convert to datetime object, format "YYYY-MM-DD HH:MM:SS"
    return timestamp

#timestamp.strftime("%Y-%m-%d %H:%M:%S")

def main():
    model = load_model()
    clean_file("results.txt")

    for location, video_files in get_video_files().items():
        print(f"Processing videos for location: {location}")
        for video in video_files:
            print(f"Processing: {video}")
            video_name = os.path.basename(video)  # Get the filename only
            timestamp = extract_timestamp(video_name)
            process_video(video, model, total_class_counter, timestamp, location)
   
    #time_of_start = datetime.strptime("2025-05-21 19:17:40", "%Y-%m-%d %H:%M:%S")
    #for video in video_files:
        #print(f"Processing: {video}")
        #process_video(video, model, total_class_counter,time_of_start,location)

if __name__ == "__main__":
    main()

#source myenv/bin/activate 