import re
from collections import Counter
from config import direction_summary, average_speeds_summary

def clean_file(file):
    with open(file, "w") as f:
        f.write("")

def save_results_to_file(video_file, detected_vehicles, class_counter, total_class_counter, output_file="results.txt"):
    with open(output_file, "a") as f:
        f.write(f"\n==== RESULTS FOR {video_file} ====\n")
        f.write(f"Total Unique Detections: {len(detected_vehicles)}\n")

        f.write("\nVehicle Type Summary\n")
        for class_name, count in class_counter.items():
            f.write(f"Class: {class_name}, Count: {count}\n")
            total_class_counter[class_name] += count

        # Initialize direction counters
        final_directions = {"N": 0, "S": 0, "E": 0, "W": 0, "NE": 0, "NW": 0, "SE": 0, "SW": 0}

        # Count only the most common direction for each vehicle
        for track_id, directions in direction_summary.items():
            if directions:
                most_common_direction = Counter(directions).most_common(1)[0][0]  # Get most common direction
                final_directions[most_common_direction] += 1  

        f.write("\nDirection Summary:\n")
        for direction, count in final_directions.items():
            f.write(f"{direction}: {count}\n")

        f.write("\nSpeed Summary:\n")
        for class_name, speeds in average_speeds_summary.items():
            if speeds:
                avg_speed = sum(speeds) / len(speeds)
                f.write(f"{class_name}: {avg_speed:.2f} Km/h\n")
        
        f.write(f"=========================\n")