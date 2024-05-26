import cv2

# Inicializar el clasificador de detección de objetos
object_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar el tracker de objetos KCF
tracker = cv2.TrackerKCF_create()

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Definir una región de interés (ROI) inicial vacía
roi = None

while True:
    # Leer un nuevo fotograma del video
    ret, frame = cap.read()
    
    # Convertir a escala de grises para el procesamiento más eficiente
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar objetos en el fotograma
    objects = object_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Selecionar el primer objeto detectado como ROI
    if len(objects) > 0 and roi is None:
        roi = tuple(objects[0])
        tracker.init(frame, roi)
    
    # Si se ha seleccionado un ROI, realizar seguimiento
    if roi is not None:
        # Actualizar el tracker con el fotograma actual
        success, roi = tracker.update(frame)
        
        # Convertir las coordenadas del ROI a valores enteros
        (x, y, w, h) = tuple(map(int, roi))
        
        # Dibujar un rectángulo alrededor del objeto seguido
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Mostrar el fotograma con el seguimiento de objetos
    cv2.imshow('Object Tracking', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
