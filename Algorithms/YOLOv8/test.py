def background_process():
    import cv2
    from ultralytics import YOLO
    from datetime import datetime
    from PIL import Image
    import sys
    import io

    image_path = r"uploads/image-test.jpg"  # Update to your image file location
    output_folder = 'public/images//'  # Update to your desired output folder location

    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to read the input image.")
        exit()

    H, W, _ = image.shape

    model_path = r"../Algorithms/YOLOv8/last.pt"  # Update to your model file location

    # Load a model
    model = YOLO(model_path)  # load a custom model

    threshold = 0.5
    itemsInScene = []
    # Perform object detection on the image
    results = model(image, verbose = False)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            if (results.names[int(class_id)] not in itemsInScene):
                itemsInScene.append(results.names[int(class_id)])
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Construct the output image filename with date and time
    output_filename = "test.jpg"
    output_path = output_folder + output_filename
    # Save the output image
    cv2.imwrite(output_path, image)
    
    for item in itemsInScene:
        print(item)

if __name__ == "__main__":
    background_process()