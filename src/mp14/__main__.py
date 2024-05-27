import RPi.GPIO as GPIO
from telegrambot import enviarMensaje, enviarDocumento
import time
import sys
import os
import cv2
import imageio
import server

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False


def deteccio_camara():
    # Inicializar el clasificador de detección de caras
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Inicializar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    # Capturar el tiempo de inicio
    start_time = time.time()
    frame_count = 0
    frames = []

    while True:
        # Leer un nuevo fotograma del video
        ret, frame = cap.read()

        if not ret:
            break

        # Convertir a escala de grises para el procesamiento más eficiente
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar caras en el fotograma
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Dibujar rectángulos alrededor de las caras detectadas
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Agregar el fotograma a la lista de fotogramas
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Mostrar el fotograma con las caras detectadas
        cv2.imshow("Face Detection", frame)

        # Salir del bucle si se presiona la tecla 'q' o si han pasado 20 segundos
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Verificar si han pasado 20 segundos desde el inicio de la grabación
        if time.time() - start_time >= 20:
            break

    # Liberar la captura de video y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    # Guardar la lista de fotogramas como un archivo de video
    output_file = "output.mp4"
    imageio.mimsave(output_file, frames, fps=15)


try:
    print("Esperant moviment...")
    while True:
        if GPIO.input(PIR_PIN):
            if not deteccio_activa:
                deteccio_camara()
                print(
                    "S'ha detectat moviment! Mira el telegram per a veure el que ha gravat la càmara"
                )
                enviarMensaje(
                    "S'ha detectat moviment en la teva càmara!, Mira el que ha gravat (Ho pots mirar també a la pàgina web:"
                )
                enviarDocumento("./videos/test.mp4")
                server
                deteccio_activa = True
                time.sleep(20)
        else:
            deteccio_activa = False  # Restableix l'estat de detecció
        time.sleep(0.1)  # Espera 0.1 segons abans de tornar a comprovar
except KeyboardInterrupt:
    print("\nS'ha interromput l'execució del programa.")
finally:
    GPIO.cleanup()  # Restaura la configuració dels pins GPIO
