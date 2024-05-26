# Sistema de càmera amb bot de telegram - E3 Security

Aquest projecte consisteix en un sistema de vigilància que detecta moviment mitjançant un sensor PIR, grava el vídeo amb una càmera, i envia notificacions amb el vídeo gravat a través d'un bot de Telegram. A més, es pot visualitzar el vídeo guardat a través d'un servidor de pàgina web.

## Requisits

- Raspberry Pi 4
- Sensor PIR
- Càmera compatible amb Raspberry Pi
- Connexió a internet (per a la hipotètica pàgina web)
- Paquets, dependències i llibreries usades:
    - **requests**: certifi chardet idna urllib3 pyOpenSSL cryptography six
    - **opencv**: numpy opencv-python-headless
    - **imageio**: imageio[ffmpeg], pillow>=8.3.2, numpy
    - **flask**: Jinja2>=3.1.2, Werkzeug>=3.0.0, blinker>=1.6.2, itsdangerous>=2.1.2, click>=8.1.3, MarkupSafe>=2.0
- Servidor de pàgina web per a visualitzar els vídeos

## Configuració del sistema

### Maquinari

1. Connecta el sensor PIR a la Raspberry Pi:
   - VCC del sensor PIR a un pin de 5V de la Raspberry Pi.
   - GND del sensor PIR a un pin GND de la Raspberry Pi.
   - Pin de senyal del sensor PIR al pin GPIO 18 de la Raspberry Pi.

2. Connecta la càmera compatible amb la Raspberry Pi al connector CSI.

### Programari

#### Instal·lació de dependències

Instal·la les següents dependències utilitzant pip:

```bash
pip install requests certifi chardet idna urllib3 pyOpenSSL cryptography six numpy opencv-python-headless imageio[ffmpeg]
```

## Estructura del projecte

```css
PROJECTE_RASPBERRY/
│
├── main.py
├── telegrambot.py
├── index.html
└── output.mp4 (exemple de vídeo gravat)
```

## Codi Principal

### main.py

```python
import RPi.GPIO as GPIO
from telegrambot import enviarMensaje, enviarDocumento
import time
import sys
import os
import cv2
import imageio

# Defineix el pin GPIO al qual està connectat el pin SIGNAL del sensor
PIR_PIN = 18

# Configura els pins GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Inicialitza la variable per controlar l'estat de detecció
deteccio_activa = False

def deteccio_camara():
    # Inicialitzar el classificador de detecció de cares
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Inicialitzar la captura de vídeo des de la càmera
    cap = cv2.VideoCapture(0)

    # Verificar si la càmera s'ha obert correctament
    if not cap.isOpened():
        print("Error al obrir la càmera")
        exit()

    # Capturar el temps d'inici
    start_time = time.time()
    frames = []

    while True:
        # Llegir un nou fotograma del vídeo
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Convertir a escala de grisos per al processament més eficient
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar cares en el fotograma
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Dibuixar rectangles al voltant de les cares detectades
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Afegir el fotograma a la llista de fotogrames
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Mostrar el fotograma amb les cares detectades
        cv2.imshow('Face Detection', frame)
        
        # Sortir del bucle si s'apreta la tecla 'q' o si han passat 20 segons
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Verificar si han passat 20 segons des de l'inici de la gravació
        if time.time() - start_time >= 20:
            break

    # Alliberar la captura de vídeo i tancar la finestra
    cap.release()
    cv2.destroyAllWindows()

    # Guardar la llista de fotogrames com un arxiu de vídeo
    output_file = 'output.mp4'
    imageio.mimsave(output_file, frames, fps=15)

try:
    print("Esperant moviment...")
    while True:
        if GPIO.input(PIR_PIN):
            if not deteccio_activa:
                deteccio_camara()
                print("S'ha detectat moviment! Mira el telegram per veure el que ha gravat la càmera")
                enviarMensaje("S'ha detectat moviment en la teva càmera! Mira el que ha gravat (Ho pots mirar també a la pàgina web):")
                enviarDocumento("output.mp4")
                deteccio_activa = True
                time.sleep(20)
        else:
            deteccio_activa = False  # Restablir l'estat de detecció
        time.sleep(0.1)  # Espera 0.1 segons abans de tornar a comprovar
except KeyboardInterrupt:
    print("\nS'ha interromput l'execució del programa.")
finally:
    GPIO.cleanup()  # Restaurar la configuració dels pins GPIO
```

### telegrambot.py

```python
import requests

# Col·loca aquí el token del teu bot
idBot = '6730938053:AAGjxzquj5-M1XMSDibw_JNIzCneTwk3AXc'
# Col·loca aquí el ID del grup on vols publicar
idGrupo = '-4093496817'

def enviarMensaje(mensaje):
    requests.post('https://api.telegram.org/bot' + idBot + '/sendMessage',
              data={'chat_id': idGrupo, 'text': mensaje, 'parse_mode': 'HTML'})

def enviarDocumento(ruta):
    requests.post('https://api.telegram.org/bot' + idBot + '/sendDocument',
              files={'document': (ruta, open(ruta, 'rb'))},
              data={'chat_id': idGrupo, 'caption': ' Resultats camera'})
```
# Pàgina web

## Descripció

La pàgina web permetrà als usuaris veure els vídeos gravats pel sistema de vigilància. La pàgina es pot implementar amb un servidor web simple que llisti els arxius de vídeo disponibles i permeti la seva visualització.

## Implementació

### Index.html

```html
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E3Security camera screen direct</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            color: #0056b3;
            margin-bottom: 20px;
        }
        video {
            max-width: 70%;
            border: 5px solid #0056b3;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        footer {
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Vídeo guardat de la càmera de vigilància</h1>
        <video id="video" controls loop>
            <source src="output.mp4" type="video/mp4">
            <source src="test.mp4" type="video/mp4">
            El teu navegador no admet la reproducció de vídeo.
        </video>
    </div>
    <footer>
        &copy; 2024 E3Security. Tots els drets reservats.
    </footer>
</body>
</html>
```

### Servidor web simple (server.py)

```python
from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

# Ruta on es guarden els vídeos
VIDEO_DIR = './videos'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/videos/<path:path>')
def send_video(path):
    return send_from_directory(VIDEO_DIR, path)

@app.route('/videos')
def list_videos():
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
    return jsonify(videos=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

# Resultats (En procés)



# Conclusions

Aquest projecte proporciona una solució completa de vigilància que combina un sensor PIR per a la detecció de moviment, una càmera per a la gravació de vídeo, un bot de Telegram per a les notificacions i una pàgina web per a la visualització dels vídeos gravats. La implementació utilitza una Raspberry Pi com a plataforma principal i diverses llibreries de Python per a la captura i processament de vídeo, així com per a la interacció amb el bot de Telegram i la pàgina web.

Amb aquest sistema, els usuaris poden estar segurs que seran notificats immediatament quan es detecti moviment i podran veure els vídeos gravats de manera convenient a través de Telegram o d'una pàgina web.