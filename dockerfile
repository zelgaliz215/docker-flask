# Imagen base de Linux
FROM alpine:3.20

# Establecer el directorio de trabajo en el contenedr
WORKDIR /app
# Copiar todo del directorio de trabajo a la ruta /app del contenedor
COPY . /app

# Instalar python3 en el directorio de trabajo
RUN apk add --no-cache python3-dev
# Crear un entorno virtual 
RUN python3 -m venv env
# Activar entorno de trabajo en el contenedor e instalar dependencias de requirements
RUN source env/bin/activate && pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000 del contenedor
EXPOSE 5000

# Ejecutar con el shell sh el comando (-c) para activar el entorno virtal y correr el archivo src/app.py
CMD [ "sh", "-c", "source env/bin/activate && python src/app.py" ]


# Crear la imagen
# docker build -t flask-docker-img .

# Ejecutar el contenedor, --rm se borra al salir, -p bindear puerto, nombre de la imagen del contenedor
# docker run --name contenedor-prueba --rm -p 5000:5000 flask-docker-img

# docker ps para verificar el contenedor
# Ejecutar el modo interactivo con la shell ash en el id del contedor 
# docker exec -it bd46fffb7029 ash