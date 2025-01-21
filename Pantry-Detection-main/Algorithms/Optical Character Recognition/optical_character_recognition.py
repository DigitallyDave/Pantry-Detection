# pip install pillow
# pip install matplotlib
# pip install pytesseract

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image
import matplotlib.pyplot as plt

img_plot = Image.open('algorithms/optical_character_recognition/cabinet_test_1.jpg')
img_plot = img_plot.rotate(-90)
plt.imshow(img_plot)
plt.title('Original Image')

image_path = 'algorithms/optical_character_recognition/cabinet_test_1.jpg'
img = Image.open(image_path)
img.save("algorithms/optical_character_recognition/preprocessed_image1.jpg")
text = pytesseract.image_to_string("algorithms/optical_character_recognition/preprocessed_image1.jpg")
print(text)

#Image preprocess for cabinet picture 1. Grayscale
img_plot = Image.open('algorithms/optical_character_recognition/cabinet_test_1.jpg')
img_plot = img_plot.rotate(-90) # Makes image portrait
img_plot = img_plot.convert("L") # Makes grayscale 'luminance'
plt.imshow(img_plot)
plt.title('Grayscale Luminance Image')

image_path = 'algorithms/optical_character_recognition/cabinet_test_1.jpg'
img = Image.open(image_path)
img = img.convert("L")
img = img.rotate(-90)
img.save("algorithms/optical_character_recognition/preprocessed_image2.jpg")
text = pytesseract.image_to_string("algorithms/optical_character_recognition/preprocessed_image2.jpg")
print(text)

#Image preprocess for cabinet picture 1. Smooth
from PIL import ImageFilter, ImageEnhance
img_plot = Image.open('algorithms/optical_character_recognition/cabinet_test_1.jpg')
img_plot = img_plot.rotate(-90) # Makes image portrait
img_plot = img_plot.filter(ImageFilter.SMOOTH_MORE) # Smooth image by reducing high-frequency noise while perserving edges
plt.imshow(img_plot)
plt.title('Smoothed Image')

image_path = 'algorithms/optical_character_recognition/cabinet_test_1.jpg'
img = Image.open(image_path)
img = img.filter(ImageFilter.SMOOTH_MORE)
img = img.rotate(-90)
img.save("algorithms/optical_character_recognition/preprocessed_image3.jpg")
text = pytesseract.image_to_string("algorithms/optical_character_recognition/preprocessed_image3.jpg")
print(text)

#Image preprocess for cabinet picture 1. Smoothed and grayscale
img_plot = Image.open('algorithms/optical_character_recognition/cabinet_test_1.jpg')
img_plot = img_plot.rotate(-90) # Makes image portrait
img_plot = img_plot.filter(ImageFilter.SMOOTH_MORE) # Smooth image by reducing high-frequency noise while perserving edges
img_plot = img_plot.convert("L")
plt.imshow(img_plot)
plt.title('Smoothed + Grayscale Image')

image_path = 'algorithms/optical_character_recognition/cabinet_test_1.jpg'
img = Image.open(image_path)
img = img.filter(ImageFilter.SMOOTH_MORE)
img = img.convert("L")
img = img.rotate(-90)
img.save("algorithms/optical_character_recognition/preprocessed_image4.jpg")
text = pytesseract.image_to_string("algorithms/optical_character_recognition/preprocessed_image4.jpg")
print(text)

# Image preprocess for cabinet picture 3
img_plot = Image.open('algorithms/optical_character_recognition/cabinet_test_3.jpg')
img_plot = img_plot.filter(ImageFilter.SMOOTH_MORE) # Smooth image by reducing high-frequency noise while perserving edges
img_plot = img_plot.convert("L")
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)
plt.imshow(img_plot)
plt.title('Smoothed Image')

image_path = 'algorithms/optical_character_recognition/cabinet_test_3.jpg'
img = Image.open(image_path)
img = img.filter(ImageFilter.SMOOTH_MORE)
img = img.convert("L")
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)
img.save("algorithms/optical_character_recognition/preprocessed_image5.jpg")
text = pytesseract.image_to_string("algorithms/optical_character_recognition/preprocessed_image5.jpg")
print(text)