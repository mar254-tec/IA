# importar paquetes necesarios
import numpy as np
from imutils.video import VideoStream
from pyzbar import pyzbar
from pygame import mixer
import argparse
import datetime
import imutils
import time
import cv2
import threading

# construye nuestro parser de argumentos y hace el parseo de los argumentos
ap = argparse.ArgumentParser()
filename = "barcodes{date}.csv".format(date=datetime.date.today()).replace("-", "")
# ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
ap.add_argument("-o", "--output", type=str, default=filename, help="path to output CSV file containing barcodes")

args = vars(ap.parse_args())

# inicializa el video y permite que el sensor de la camara comience a escanear
print("[INFO] Iniciando video...")
# para webcam usa este>
# src=0 es la camara de la lap, src=1 es una webcam externa
vs = VideoStream(src=0).start()
# para camara de raspberri usa este otro>
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# abre un CSV para escribir la informacion de fecha y hora donde se detecta el codigo QR
csv = open(args["output"], "a")

# Arreglo de barcodes encontrados
found = set()

# Variable de tiempo para cuando escanea codigo
isWaiting = False

# Texto que se muestra en el mensaje
text = ""


# Lee el qr del cuadro
def get_qr_data(input_frame):
    try:
        # Regresa el qr decodificado
        return pyzbar.decode(input_frame)
    except:
        print("Exception")
        return []


# Dibujar cuadrado alrededor del qr
def draw_square(frame_in, qrobj):
    # Si no tiene datos regresa el frame
    if len(qrobj) == 0:
        return frame_in
    else:
        # Recorre el arreglo en busqueda del codigo decodificado
        for obj in qrobj:
            # Usamos variable global del texto
            global text
            text = obj.data.decode("utf-8")

            # Si no esta esperando escribimos el codigo en el csv
            if not isWaiting:
                write_csv(text)
            pts = obj.polygon
            pts = np.array([pts], np.int32)
            pts = pts.reshape((4, 1, 2))
            cv2.polylines(frame_in, [pts], True, (0, 255,), 2)
            cv2.putText(frame_in,text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 200, 1), 5)
            return frame_in


# Escribimos en el archivo
def write_csv(text):
    csv.write("{}, {}\n".format(datetime.datetime.now(), text))

# Variable para esperar a leer el proximo codigo
def waiting():
    global isWaiting
    isWaiting = True
    time.sleep(4)
    isWaiting = False


# loop de frames del video
while True:
    # toma el cuadro(frame) del video y le cambia el tama;o a un maximo de 400 pixeles
    frame = vs.read()
    frame = imutils.resize(frame, width=1366, height=768)

    # Encuentra los barcodes o QR y los decodifica:
    qr_obj = get_qr_data(frame)

    # Si esta esperando mostramos el cuadro de texto
    if isWaiting:
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 200, 1), 2)

    # Si tiene datos y no esta esperando dibuja el cuadrado
    if qr_obj and not isWaiting:
        draw_square(frame, qr_obj)
        barcodeData = qr_obj[0].data.decode("utf-8")

        if barcodeData not in found:
            mixer.init()
            sound = mixer.Sound('notifa440.mp3')
            sound.play()
            found.add(barcodeData)
            threading.Thread(target=waiting).start()
        else:
            mixer.init()
            sound = mixer.Sound('notifa440.mp3')
            sound.play()
            found.add(barcodeData)
            threading.Thread(target=waiting).start()
    cv2.imshow("BarcodeScanner", frame)

    # loop de los barcodes detectados

    key = cv2.waitKey(1) & 0xFF
    # waitkey originalmente tenía valor =1

    # si la tecla 'q' se puls[o, break del loop
    if key == ord("q"):
        break

# cierra el archivo CSV de salida y hace limpieza
print("[INFO] limpiando...")
csv.close()
cv2.destroyAllWindows()
vs.stop()

