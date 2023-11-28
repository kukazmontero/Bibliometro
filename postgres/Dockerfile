FROM postgis/postgis:13-3.2

# Establecer variables de entorno para credenciales de base de datos (ajústalas según tus necesidades)
ENV POSTGRES_DB=metro_santiago_3
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=passworda

# Verificar si el archivo SQL antiguo existe antes de intentar eliminarlo
RUN test -e /docker-entrypoint-initdb.d/metro_santiago.sql && rm /docker-entrypoint-initdb.d/metro_santiago.sql || true

# Copiar el archivo SQL para inicializar la base de datos
COPY metro_santiago.sql /docker-entrypoint-initdb.d/

# El contenedor ejecutará automáticamente los scripts SQL en /docker-entrypoint-initdb.d/ para inicializar la base de datos
