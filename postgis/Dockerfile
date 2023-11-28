# Dockerfile de PostGIS
FROM postgis/postgis:13-3.2

# Actualizar e instalar paquetes en build en lugar de iniciar contenedor
RUN apt-get update && apt-get install -y libpq-dev\ 
    python3 \
    python3-pip

RUN pip install geopandas matplotlib Flask

COPY visualizar_estaciones.py /
COPY run.sh /run.sh
RUN pip install SQLAlchemy psycopg2
RUN chmod +x /run.sh