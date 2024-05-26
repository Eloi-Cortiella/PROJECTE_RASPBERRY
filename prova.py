import cv2
import time

# Inicializar el clasificador de detección de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

# Obtener el ancho y alto del fotograma de video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Configuración del VideoWriter para grabar el video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para formato MP4
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# Capturar el tiempo de inicio
start_time = time.time()

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
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Grabar el fotograma en el archivo de video
    out.write(frame)
    
    # Mostrar el fotograma con las caras detectadas
    cv2.imshow('Face Detection', frame)
    
    # Salir del bucle si se presiona la tecla 'q' o si han pasado 20 segundos
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Verificar si han pasado 20 segundos desde el inicio de la grabación
    if time.time() - start_time >= 20:
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
out.release()
cv2.destroyAllWindows()
