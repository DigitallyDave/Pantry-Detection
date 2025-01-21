import os
from google.cloud import storage
from google.cloud import firestore
from ultralytics import YOLO
import cv2
import tempfile
import logging
from functions_framework import cloud_event


@cloud_event
def image_analysis(cloud_event):
    bucket_name = cloud_event.data['bucket']
    file_name = cloud_event.data['name']
    file_type = cloud_event.data['contentType']

    # Check if the uploaded file is an image
    if file_type.startswith('image/'):
        
        # Download the uploaded image file to a temporary location
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            blob.download_to_filename(temp_file.name)
            image_path = temp_file.name

        logging.info(f"Image downloaded to: {image_path}")

        # Process the image using the provided code
        image = cv2.imread(image_path)
        if image is None:
            logging.error("Error: Unable to read the image file.")
            return

        model_path = 'last.pt'
        model = YOLO(model_path)  # Load a custom model
        logging.info(f"Model loaded: {model}")

        threshold = 0.5
        detected_ingredients = {}

        logging.info("Image processing started")

        results = model(image)[0]
        for result in results.boxes.data.tolist():
            score, class_id = result[4], result[5]
            if score > threshold:
                item_name = model.names[int(class_id)].lower().strip()
                if item_name in detected_ingredients:
                    detected_ingredients[item_name] += 1
                else:
                    detected_ingredients[item_name] = 1

        logging.info("Image processing completed")
        logging.info(f"Detected ingredients: {detected_ingredients}")

        # Filter identified foods based on count threshold
        identified_foods = list(detected_ingredients.keys())

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
                
                detected_ingredients_lower = [x.lower().strip() for x in detected_ingredients]
                matching_ingredients = set(recipe_ingredients) & set(detected_ingredients.keys())
                
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