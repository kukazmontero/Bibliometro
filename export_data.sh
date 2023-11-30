#!/bin/bash

# Definir el nombre del archivo GeoJSON
GEOJSON_FILE="metro_data.geojson"

# Inicializar el archivo GeoJSON
echo '{"type":"FeatureCollection","features":[' > $GEOJSON_FILE

# Obtener datos de la base de datos y agregar estaciones al GeoJSON
docker exec -i bibliometro-postgis-1 psql -U user -d metro_santiago -t -A -F',' -c "SELECT c.estacion, c.longitud, c.latitud, l.linea FROM coordenadas c JOIN lineas_estacion l ON c.estacion = l.estacion" | \
while IFS=',' read -r estacion longitud latitud linea; do
    echo '{"type":"Feature","geometry":{"type":"Point","coordinates":['$longitud','$latitud']},"properties":{"estacion":"'$estacion'","linea":"'$linea'"}}' >> $GEOJSON_FILE
    echo ',' >> $GEOJSON_FILE
done

# Obtener datos de la base de datos y agregar conexiones al GeoJSON
docker exec -i bibliometro-postgis-1 psql -U user -d metro_santiago -t -A -F',' -c "SELECT c.estacion_origen, c.estacion_destino, c.estado FROM conexiones c" | \
while IFS=',' read -r estacion_origen estacion_destino estado; do
    echo '{"type":"Feature","geometry":{"type":"LineString","coordinates":[]},"properties":{"estacion_origen":"'$estacion_origen'","estacion_destino":"'$estacion_destino'","estado":'$estado'}}' >> $GEOJSON_FILE
    echo ',' >> $GEOJSON_FILE
done

# Eliminar la coma extra del último elemento
truncate -s-2 $GEOJSON_FILE

# Cerrar el archivo GeoJSON
echo ']}' >> $GEOJSON_FILE
