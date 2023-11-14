# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app/

# Copia los archivos necesarios al contenedor
COPY . /app/

# Imprime el contenido del directorio para verificar que los archivos se copiaron correctamente
RUN ls -la /app/

# Instala las dependencias necesarias, incluidas libpq-dev y build-essential
RUN apt-get update \
    && apt-get install -y libpq-dev build-essential \
    && pip install --trusted-host pypi.python.org Flask psycopg2 requests \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ejecuta metadata.py para inicializar la base de datos
RUN python metadata.py

# Expone el puerto 80
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]



