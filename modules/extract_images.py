from cv2 import VideoCapture, imwrite
from os import makedirs, unlink
from os.path import join

def extractImages(file, user):
    # Abre el video
    cap = VideoCapture(file)
    print(file)

    # Verifica si el video se abrió correctamente
    if not cap.isOpened():
        print("No se pudo abrir el video")
        return

    # Inicializa el contador de frames
    frame_count = 0
    path = join('img', user)
    makedirs(path)
    while True:
        # Lee el video frame por frame
        ret, frame = cap.read()

        # Si el frame se leyó correctamente ret es True
        if not ret:
            break

        # Guarda el frame como una imagen

        imwrite(join(path, 'frame{:d}.jpg'.format(frame_count)), frame)

        # Incrementa el contador de frames
        frame_count += 1

    # Cierra el video
    cap.release()