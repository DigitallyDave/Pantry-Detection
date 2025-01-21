import os
from ultralytics import YOLO
import cv2
from google.cloud import storage

def annotate_frame(event, context):
    # Get the bucket and file information from the triggered event
    bucket_name = event['bucket']
    file_name = event['name']
    
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    
    # Download the video file from the source bucket
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    video_path = '/tmp/' + file_name
    blob.download_to_filename(video_path)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return
    
    # Load the YOLOv8 model
    model_path = 'last.pt'
    model = YOLO(model_path)
    threshold = 0.5
    
    frame_count = 0
    annotated_frame = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % 10 == 0:
            results = model(frame)[0]
            
            if len(results.boxes.data) > 0:
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    if score > threshold:
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                        cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
                annotated_frame = frame
                break
        
        frame_count += 1
    
    cap.release()
    
    if annotated_frame is None:
        print("No items detected in the video.")
        return
    
    # Save the annotated frame as an image file
    output_file_name = 'annotated_frame.jpg'
    output_path = '/tmp/' + output_file_name
    cv2.imwrite(output_path, annotated_frame)
    
    # Upload the annotated frame to the destination bucket
    destination_bucket_name = 'rummage-annotated'
    destination_bucket = storage_client.get_bucket(destination_bucket_name)
    blob = destination_bucket.blob(output_file_name)
    blob.upload_from_filename(output_path)
    
    # Clean up temporary files
    os.remove(video_path)
    os.remove(output_path)