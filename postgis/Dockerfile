FROM postgis/postgis:13-3.2

# Establecer variables de entorno para credenciales de base de datos (ajústalas según tus necesidades)
ENV POSTGRES_DB=metro_santiago_3
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

# Copiar el archivo SQL principal para inicializar la base de datos desde la carpeta postgres
#COPY ../postgres/metro_santiago.sql /docker-entrypoint-initdb.d/

# Copiar el archivo SQL para generar vistas desde la carpeta postgis
COPY crear_vistas.sql /docker-entrypoint-initdb.d/


# El contenedor ejecutará automáticamente los scripts SQL en /docker-entrypoint-initdb.d/ para inicializar la base de datos
