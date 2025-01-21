import os
import cv2

def convert_to_grayscale(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    files = os.listdir(input_folder)

    for file in files:
        input_path = os.path.join(input_folder, file)
        image = cv2.imread(input_path)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        output_path = os.path.join(output_folder,file)
        cv2.imwrite(output_path, grayscale)
        print(f"Converted {file} to grayscale and saved to {output_path}")

input_folder = r"D:\data\images\validation"
output_folder = r"D:\data\images_gray\validation"
convert_to_grayscale(input_folder, output_folder)