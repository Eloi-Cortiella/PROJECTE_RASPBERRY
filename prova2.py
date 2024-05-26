import cv2
import numpy as np
from libcamera import PipelineHandler, CameraManager

# Inicializar el gestor de cámaras
camera_manager = CameraManager()

# Obtener la cámara predeterminada
camera = camera_manager.get()

# Configurar el formato y la resolución
camera_configuration = camera.generate_configuration()
camera_configuration.set_option("format", "RGB24")
camera_configuration.set_option("width", 640)
camera_configuration.set_option("height", 480)
camera.configure(camera_configuration)

# Inicializar el gestor de la tubería
pipeline_handler = PipelineHandler(camera)

# Capturar un fotograma
buffer = pipeline_handler.get()
image = np.ndarray(buffer.planes[0].size.height,
                   buffer.planes[0].size.width,
                   buffer.planes[0].data, dtype=np.uint8)

# Convertir la imagen a formato OpenCV (BGR)
image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Mostrar la imagen
cv2.imshow("Image", image_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
