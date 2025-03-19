import re

def clean_file(file):
    with open(file, "w") as f:
        f.write("")

def save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter, output_file="results.txt"):
    with open(output_file, "a") as f:
        f.write(f"\n==== RESULTS FOR {video_file} ====\n")
        f.write(f"Total Unique Detections: {len(detected_vehicles)}\n")
        for class_name, count in class_counter.items():
            f.write(f"Class: {class_name}, Count: {count}\n")
            total_class_counter[class_name] += count
