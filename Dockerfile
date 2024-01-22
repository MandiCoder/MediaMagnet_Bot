# Usa una imagen base de Python
FROM python:3.10.13

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia los archivos de requerimientos al contenedor
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Especifica el comando que se ejecutará al iniciar el contenedor
CMD ["python", "./main.py"]
