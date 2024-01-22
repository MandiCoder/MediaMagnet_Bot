# Usa una imagen base de Python
FROM python:3.10.13

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | sh
ENV PATH="${PATH}:/root/.poetry/bin"

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia solo el archivo de bloqueo de dependencias y el archivo pyproject.toml
COPY pyproject.toml ./

# Instala las dependencias usando Poetry
RUN poetry install --no-dev

# Copia el resto de los archivos al contenedor
COPY . .

# Especifica el comando que se ejecutará al iniciar el contenedor
CMD ["poetry", "run", "python", "./main.py"]
