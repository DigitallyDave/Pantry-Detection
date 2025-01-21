import os
from ultralytics import YOLO
import cv2

video_path = r"D:\Test Videos\annotate_test.mp4" #update to your file location
video_path_out = r'D:\Test Videos\annotate_small_model.mp4'

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

ret, frame = cap.read()
if frame is None:
    print("Error: Unable to read the first frame from the video.")
    exit()

H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = r"Algorithms\YOLOv8\weights\small_model_testing_annotate.pt" #update to your file location

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.0

while ret:
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

# Wait for a key press before closing OpenCV windows

cap.release()
out.release()
