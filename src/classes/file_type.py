class fileType():
    def __init__(self, file: str) -> None:
        """
        El código define una clase con métodos para verificar si un archivo determinado es un video o
        una foto en función de su extensión de archivo.

        :param file: El parámetro `archivo` es una cadena que representa el nombre o la ruta de un
        archivo
        :type file: str
        """

        self.file = file.strip()

    def isVideo(self):
        # El código verifica si la extensión de archivo del archivo dado es 'mp4', 'mkv' o '3gp'. Si
        # alguna de estas condiciones es verdadera, devuelve True, lo que indica que el archivo es un
        # video.
        if self.file.endswith('.mp4') or self.file.endswith('.mkv') or self.file.endswith('.3gp'):
            return True
        else:
            return False

    def isPhoto(self):
        # El código verifica si la extensión del archivo dado es 'jpg', 'png' o 'jpeg'. Si alguna de
        # estas condiciones es verdadera, devuelve True, lo que indica que el archivo es una foto.
        if self.file.endswith('.jpg') or self.file.endswith('.png') or self.file.endswith('.jpeg'):
            return True
        else:
            return False