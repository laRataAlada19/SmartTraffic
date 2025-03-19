from config import video_files, ground_truth,total_class_counter
from model import load_model
from video_processing import process_video
from file_operations import clean_file

def main():
    model = load_model()
    clean_file("results.txt")

    for video in video_files:
        print(f"Processing: {video}")
        process_video(video, model, ground_truth, total_class_counter)

if __name__ == "__main__":
    main()
