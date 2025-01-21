import os
from ultralytics import YOLO
import cv2
import random
import string

video_path = r"D:\Test Videos\original_4.mp4" # update to your file location

cap = cv2.VideoCapture(video_path) # opens the video path as cap and is now accessible as frames

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

ret, frame = cap.read() # access first frame

if frame is None:
    print("Error: Unable to read the first frame from the video.")
    exit()

H, W, _ = frame.shape # retrieves pixel dimensions of the frame

model_path = r"Algorithms\YOLOv8\weights\april_6.pt" 

model = YOLO(model_path)  # loads custom model from path

box_color = (0, 255, 0) # annotation box color and thickness
box_thickness = 2

image_name = '' #initialize image_name so that previous_name doesnt throw error for first frame

# LOOP THROUGH VIDEO
# while ret -> while the frames are still available from cap
while ret:
    previous_name = image_name #set previous name to the image name before changing
    image_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6)) # randomize image name

    text_path = r"C:\Users\colet\Documents\Annotated Data\labels\{}.txt".format(image_name) # location where text file will be written to and saved

    original_frame = frame.copy() # copy the frame without boxes drawn so that it can be saved as a clean file

    results = model(frame)[0] # results are all the objects found in each frame -> run for loop over each item
    for result in results.boxes.data.tolist():

        x1, y1, x2, y2, score, class_id = result # retrieve the coordinates of the boxes as well as class_id/score

        # YOLO formatting -> calculate the center x,y position of the box and width,height
        x_center = (x1 + x2) / (2 * W) 
        y_center = (y1 + y2) / (2 * H)
        box_width = (x2 - x1) / W
        box_height = (y2 - y1) / H

        # Add rectangle to the frame with the box color and thickness
        # Also place text on each box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), box_color, box_thickness)
        cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
        # Open the text file created earlier and add the YOLO formatted class, coordinates, and dimensions
        with open(text_path, "a") as f:
            f.write(f"{int(class_id)} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

    # DISPLAY POP UP FOR REVIEW
    # If the video is landscape make the width 800 otherwise width is 300 and resize frame for display
    aspect_ratio = W / H
    if W > H:
        desired_width = 800
    else:
        desired_width = 300
    desired_height = int(desired_width/aspect_ratio)
    resized_frame = cv2.resize(frame, (desired_width, desired_height))

    # Display the frame with options for saving, deleting previous and saving, deleting previous and saving and skipping
    cv2.imshow("Press 's' to save | 'a' to delete previous and save current | 'd' to delete previous and skip", resized_frame) 

    # Wait for key event
    key = cv2.waitKey(0)

    annotated_path = r"C:\Users\colet\Documents\Annotated Data\images\{}.png".format(image_name)
    raw_path = r"C:\Users\colet\Documents\Raw Data\{}.png".format(image_name)

    previous_path = r"C:\Users\colet\Documents\Annotated Data\images\{}.png".format(previous_name)
    previous_text = r"C:\Users\colet\Documents\Annotated Data\labels\{}.txt".format(previous_name)
    # Pressing 's' saved the image to the annotated_path, does not need to save text because it gets automatically created
    if key == ord('s'):
        cv2.imwrite(annotated_path, original_frame)
        print("Saved Image: {}.png".format(image_name))
    # Pressing 'd' removes the previous text file saved and previous image file saved
    # It also skips the current frame (deleting the text file that is auto created)
    elif key == ord('d') and os.path.exists(previous_path):
        if os.path.exists(previous_text):
            os.remove(previous_text)
            print("Deleted Text: {}.txt".format(previous_name))
        os.remove(previous_path)
        print("Deleted Image: {}.png".format(previous_name))
        if os.path.exists(text_path):
            os.remove(text_path)
            print("Deleted Text: {}.txt".format(image_name))
    # Pressing 'a' removes the previous text file saved and the previous image file saved
    # Afterwards, it saves the current frame (the associated text file is saved earlier)
    elif key == ord('a'):
        if os.path.exists(previous_text):
            os.remove(previous_text)
            print("Deleted Text: {}.txt".format(previous_name))
        if os.path.exists(previous_path):
            os.remove(previous_path)
            print("Deleted Image: {}.png".format(previous_name))
        cv2.imwrite(annotated_path,original_frame)
        print("Saved Image: {}.png".format(image_name))
    # if any other key is pressed then simply skip the current frame. Need to
    # delete the text file that is auto created and write the frame to the raw bucket
    elif os.path.exists(text_path):
        os.remove(text_path)
        cv2.imwrite(raw_path, original_frame)
        print("Image saved to raw data: {}.png".format(image_name))
    ret, frame = cap.read()

cap.release()
