import cv2

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)  # 0 representa la cámara predeterminada del sistema

while True:
    # Leer un nuevo fotograma del video
    ret, frame = cap.read()
    
    # Mostrar el fotograma
    cv2.imshow('Video', frame)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
