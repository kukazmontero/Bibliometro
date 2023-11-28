# Dockerfile de postgis

FROM postgis/postgis:13-3.2

# Instalar paquetes adicionales necesarios para visualización
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Instalar bibliotecas de Python
RUN pip3 install geopandas matplotlib Flask

# Crear un directorio para almacenar la imagen en el host
RUN mkdir -p /output
