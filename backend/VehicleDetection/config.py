from collections import defaultdict

video_files = ["1.mp4", "2.mp4", "3.mp4", "4.mp4", "5.mp4"]
total_class_counter = defaultdict(int)

ground_truth = {
    "1.mp4": {"car": 37, "motorcycle": 1},
    "2.mp4": {"car": 205, "truck": 27, "motorcycle": 3},
    "3.mp4": {"car": 11, "motorcycle": 4, "bike": 2, "truck": 3},
    "4.mp4": {"car": 59, "motorcycle": 68, "truck": 3},
    "5.mp4": {"car": 33, "bus": 1, "truck": 1}
}
