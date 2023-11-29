from random import randint
from os.path import splitext, basename
from cv2 import (
    VideoCapture,
    resize,
    addWeighted,
    imwrite,
    CAP_PROP_FRAME_COUNT,
    CAP_PROP_POS_FRAMES,
    CAP_PROP_FPS,
)

def extractInfoVideo(file: str, username: str):
    """
    La función `extractInfoVideo` toma un archivo de video y un nombre de usuario como entrada, extrae
    información sobre el video (como el número de fotogramas y la duración), genera una imagen en
    miniatura con una marca de agua basada en el nombre de usuario y devuelve la ruta a la imagen en
    miniatura y la duración del video en segundos.

    :param file: El parámetro `archivo` es la ruta al archivo de video del que desea extraer
    información. Debe ser una cadena que represente la ruta del archivo
    :param username: El parámetro `username` es una cadena que representa el nombre de usuario del
    usuario que solicita la extracción de la miniatura del video
    :return: el nombre de archivo de la imagen en miniatura del video generado y la duración del video
    en segundos.
    """
    VIDEO = VideoCapture(file)  # RUTA DEL VIDEO
    frames = VIDEO.get(CAP_PROP_FRAME_COUNT)
    fps = int(VIDEO.get(CAP_PROP_FPS))
    seconds = int(frames / fps)

    try:
        TOTALFRAME = int(VIDEO.get(CAP_PROP_FRAME_COUNT))
        VIDEO.set(CAP_PROP_POS_FRAMES, TOTALFRAME // randint(5, 15))
        IMG = VIDEO.read()[1]
        Alto, Ancho = IMG.shape[:2]
        if Ancho > Alto:
            Alto = int(Alto * 320 / Ancho)
            Ancho = 320
        else:
            Ancho = int(Ancho * 320 / Alto)
            Alto = 320

        IMG = resize(IMG, (Ancho, Alto))
        overlay = IMG.copy()
        alpha = 0.5

        output = addWeighted(
            overlay, alpha, IMG[Alto - Alto : Alto, Ancho - Ancho : Ancho], 1 - alpha, 0
        )
        
        imwrite(splitext(basename(file))[0] + ".jpg", output)
        return splitext(basename(file))[0] + ".jpg", seconds
    except Exception as x:
        print(x)
        return "./assets/thumb.jpg", seconds