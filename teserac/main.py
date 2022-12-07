from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np
#define la ruta al archivo tessaract.exe
ruta_tessaract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#Define ruta a la imagen
ruta_imagen = 'img/ruido.jpg'

# get grayscale image
#def get_grayscale(ruta_imagen):
    #return cv2.cvtColor(ruta_imagen, cv2.COLOR_BGR2GRAY)
#img1 = Image.open(ruta_imagen)
img = cv2.imread(ruta_imagen)
# noise removal
def remove_noise(image):
     return cv2.medianBlur(image, 5)

#Apuntar tessaract_cmd a la ruta de tessaract.exe
pytesseract.tesseract_cmd = ruta_tessaract

#configurar idiomas
idioma_greek = r'-l grc --psm 6'
idioma_frances = r'-l fra --psm 6'
idioma_spanish = r'-l spa --psm 6'
#Abre la imagen con PIL *Python Imaging Library* o "Pillow"
#img = Image.open(ruta_imagen)
img = remove_noise(img)
#Extrae el texto de la imagen, dependiendo del idioma
#text = pytesseract.image_to_string(img,config=idioma_greek)

#Extrae el texto de la imagen
text = pytesseract.image_to_string(img)
print(text)
