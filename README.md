# Sistema de càmera amb bot de telegram

Aquest projecte consisteix en un sistema de vigilància que detecta moviment mitjançant un sensor PIR, grava el vídeo amb una càmera, i envia notificacions amb el vídeo gravat a través d'un bot de Telegram. A més, es pot visualitzar el vídeo guardat a través d'una pàgina web.

## Requisits

- Raspberry Pi
- Sensor PIR
- Càmera compatible amb Raspberry Pi
- Connexió a internet
- Llibreries Python: `RPi.GPIO`, `cv2` (OpenCV), `telegrambot`
- Pàgina web per a visualitzar els vídeos

## Configuració del sistema

### `main.py`

Aquest script principal gestiona la detecció de moviment mitjançant el sensor PIR i coordina l'enviament de notificacions i vídeos a través de Telegram.

```python
import RPi.GPIO as GPIO
from telegrambot import enviarMensaje, enviarDocumento
import time
import sys
import os
import cv2
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False

def deteccio_camara():
    # Inicializar el clasificador de detección de caras
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Inicializar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    while True:
        # Leer un nuevo fotograma del video
        ret, frame = cap.read()
        
        # Convertir a escala de grises para el procesamiento más eficiente
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar caras en el fotograma
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Dibujar rectángulos alrededor de las caras detectadas
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Mostrar el fotograma con las caras detectadas
        cv2.imshow('Face Detection', frame)
        
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la captura de video y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

try:
    print("Esperant moviment...")
    while True:
        if GPIO.input(PIR_PIN):
            if not deteccio_activa:
                deteccio_camara()
                print("S'ha detectat moviment! Mira el telegram per a veure el que ha gravat la càmara")
                enviarMensaje("S'ha detectat moviment en la teva càmara!, Mira el que ha gravat (Ho pots mirar també a la pàgina web:")
                enviarDocumento("./test.mp4")
                deteccio_activa = True
        else:
            deteccio_activa = False  # Restableix l'estat de detecció
        time.sleep(0.1)  # Espera 0.1 segons abans de tornar a comprovar
except KeyboardInterrupt:
    print("\nS'ha interromput l'execució del programa.")
finally:
    GPIO.cleanup()  # Restaura la configuració dels pins GPIO

```