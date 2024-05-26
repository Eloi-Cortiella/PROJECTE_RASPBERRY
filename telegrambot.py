import requests

# Coloca aquí el token de tu bot
idBot = '6730938053:AAGjxzquj5-M1XMSDibw_JNIzCneTwk3AXc'
# Coloca aquí el ID del grupo donde quieres publicar
idGrupo = '-4093496817'

def enviarMensaje(mensaje):
    requests.post('https://api.telegram.org/bot' + idBot + '/sendMessage',
              data={'chat_id': idGrupo, 'text': mensaje, 'parse_mode': 'HTML'})

def enviarDocumento(ruta):
    requests.post('https://api.telegram.org/bot' + idBot + '/sendDocument',
              files={'document': (ruta, open(ruta, 'rb'))},
              data={'chat_id': idGrupo, 'caption': ' Resultats camera'})

# Ejemplo de uso
enviarMensaje("Hola, soy un bot y estoy mandando un mensaje a Telegram usando Python")
enviarDocumento("./test.mp4")