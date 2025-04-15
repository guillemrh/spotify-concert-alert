# Base image
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos del proyecto a nuestro contenedor
COPY requirements.txt .

# Instalamos las herramientas necesarias para construir dependencias
RUN pip install --no-cache-dir setuptools wheel
# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código al contenedor
COPY .. ./spotify_client/

# Set PYTHONPATH
ENV PYTHONPATH="/spotify_client"

# Ejecutamos el script principal
CMD ["python", "spotify_client/app/spotify_client.py"]