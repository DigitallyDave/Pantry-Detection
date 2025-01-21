import os
from ultralytics import YOLO
import cv2
import random
import string

image_path = r"C:\Users\colet\Documents\Annotated Data\images\multi.png"

image_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
text_path = r"C:\Users\colet\Documents\Annotated Data\labels\{}.txt".format(image_name)
frame = cv2.imread(image_path)
original_frame = frame.copy()
H, W, _ = frame.shape
box_color = (0, 255, 0)  # Green color
box_thickness = 2
model_path = r"Algorithms\YOLOv8\april_6.pt" #update to your file location

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5
results = model(frame)[0]
print(f"Frame (width x height): {W} x {H}")
for result in results.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = result
    x_center = (x1 + x2) / (2 * W)
    y_center = (y1 + y2) / (2 * H)
    box_width = (x2 - x1) / W
    box_height = (y2 - y1) / H
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), box_color, box_thickness)
    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    print(f"x center: {x_center}")
    print(f"y center: {y_center}")
    print(f"Width: {box_width}")
    print(f"Height: {box_height}")
    with open(text_path, "a") as f:
        f.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")


# Display the image with the bounding box
aspect_ratio = W / H
if W > H:
    desired_width = 800
else:
    desired_width = 300
desired_height = int(desired_width/aspect_ratio)
resized_frame = cv2.resize(frame, (desired_width, desired_height))
cv2.imshow("Image with Bounding Box", resized_frame)

# Wait for key event
key = cv2.waitKey(0)

file_path = r"C:\Users\colet\Documents\Annotated Data\images\{}.png".format(image_name)
# Check if the key pressed is 's' (to save the image)
if key == ord('s'):
    cv2.imwrite(file_path, original_frame)
    print("Image saved successfully.")
    # Write bounding box coordinates to a text file in YOLO format

cv2.destroyAllWindows()