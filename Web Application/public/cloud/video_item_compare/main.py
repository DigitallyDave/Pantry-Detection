import os
from google.cloud import storage
from google.cloud import firestore
from ultralytics import YOLO
import cv2
import tempfile
import logging
from functions_framework import cloud_event

@cloud_event
def video_analysis(cloud_event):

    bucket_name = cloud_event.data['bucket']
    file_name = cloud_event.data['name']
    file_type = cloud_event.data['contentType']

    # Check if the uploaded file is a video
    if file_type.startswith('video/'):

        # Download the uploaded video file to a temporary location
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            blob.download_to_filename(temp_file.name)
            video_path = temp_file.name
        
        logging.info(f"Video downloaded to: {video_path}")
        
        # Process the video using the provided code
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error("Error: Unable to open video file.")
            return

        model_path = 'last.pt'
        model = YOLO(model_path)  # Load a custom model
        logging.info(f"Model loaded: {model}")

        threshold = 0.5
        detected_ingredients = {}

        logging.info("Video processing started")

        frame_count = 0
        frame_skip = 7 # Process 1 out of every 7 frames

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_skip == 0:
                results = model(frame)[0]
                for result in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = result
                    if score > threshold:
                        item_name = model.names[int(class_id)].upper()
                        if item_name in detected_ingredients:
                            detected_ingredients[item_name] += 1
                        else:
                            detected_ingredients[item_name] = 1
            
            frame_count += 1

        cap.release()
        
        logging.info("Video processing completed")
        logging.info(f"Detected ingredients: {detected_ingredients}")
        
        # Filter identified foods based on count threshold
        identified_foods = [item for item, count in detected_ingredients.items() if count >= 3]

        # Capitalize the first letter of each word in the identified foods
        identified_foods = [' '.join(word.capitalize() for word in food.split()) for food in identified_foods]

        
        try:
            # Query Firestore for recipes matching the detected ingredients
            db = firestore.Client(project="rummage-4800d", database="recipes")
            recipes_collection = db.collection('recipes')
            
            logging.info("Starting Firestore query")
            
            matching_recipes = []
            
            for recipe_doc in recipes_collection.stream():
                logging.info(f"Processing recipe: {recipe_doc.id}")
                
                recipe_data = recipe_doc.to_dict()
                recipe_ingredients = [value.lower().strip() for key, value in recipe_data.items() if key.startswith('Ingredient')]
                
                identified_foods_lower = [x.lower().strip() for x in identified_foods]
                matching_ingredients = set(recipe_ingredients) & set(identified_foods_lower)
                
                completeness = len(matching_ingredients) / len(recipe_ingredients) * 100

                # If completeness atleast 75%
                if completeness >= 70:
                    matching_recipes.append((recipe_doc.id, completeness))
            
            logging.info("Firestore query and matching completed")
            
            # Sort the matching recipes by completeness in descending order
            matching_recipes.sort(key=lambda x: x[1], reverse=True)
            
            logging.info("Generating output content")
            
            # Write the identified foods and matching recipes to Firestore
            db = firestore.Client(project="rummage-4800d", database="recipes")
            results_collection = db.collection('processing_results')
            result_doc = results_collection.document(file_name)
            
            result_data = {
                'identified_foods': identified_foods,
                'matching_recipes': [{'name': recipe, 'completeness': completeness} for recipe, completeness in matching_recipes]
            }
            
            result_doc.set(result_data)

            logging.info("Output content written to Firestore")

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            raise
            