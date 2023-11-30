# Nombre del archivo GeoJSON de entrada
METRO_GEOJSON="metro_data.geojson"
# Nombre del archivo GeoJSON de salida con la ruta
METRO_ASTAR_ROUTE_GEOJSON="metro_data_with_astar_route.geojson"

# ... (Tu código actual para generar el GeoJSON)

# Crear tabla de vértices solo si no existe
docker exec -i bibliometro-postgis-1 psql -U user -d metro_santiago -c "
    CREATE TABLE IF NOT EXISTS vertices AS
    SELECT row_number() OVER () AS id, estacion, longitud, latitud
    FROM coordenadas;
"

# Crear tabla de bordes solo si no existe
docker exec -i bibliometro-postgis-1 psql -U user -d metro_santiago -c "
    CREATE TABLE IF NOT EXISTS conexiones_edges AS
    SELECT
        e.id,
        v1.id AS source,
        v2.id AS target,
        e.estado AS cost
    FROM
        conexiones e
        JOIN vertices v1 ON e.estacion_origen = v1.estacion
        JOIN vertices v2 ON e.estacion_destino = v2.estacion;
"

# Consultar ruta usando A* y escribir el GeoJSON
docker exec -i bibliometro-postgis-1 psql -U user -d metro_santiago -t -A -F',' -c "
    SELECT
        seq,
        v.estacion,
        v.linea,
        v.tipo,
        ST_AsGeoJSON(ST_Transform(ST_SetSRID(v.coordenadas, 4326), 4326))::json AS geometry
    INTO TEMPORARY TABLE astar_route
    FROM (
        SELECT
            seq,
            e.node AS node,
            e.edge AS edge,
            v.estacion,
            v.linea,
            v.tipo,
            v.longitud,
            v.latitud,
            e.cost
        FROM pgr_astar(
            'SELECT id, source, target, cost FROM conexiones_edges',
            (SELECT id FROM vertices WHERE estacion = 'san pablo'),
            (SELECT id FROM vertices WHERE estacion = 'los heroes'),
            false, false
        ) AS e
        JOIN vertices v ON e.node = v.id
    ) AS astar_route;

    -- Escribir el GeoJSON
    COPY (
        SELECT * FROM astar_route
    ) TO '/path/to/$METRO_ASTAR_ROUTE_GEOJSON' WITH CSV HEADER;

    -- Concatenar el archivo GeoJSON de ruta con el archivo original
    cat '/path/to/$METRO_GEOJSON' '/path/to/$METRO_ASTAR_ROUTE_GEOJSON' > '/path/to/$METRO_ASTAR_ROUTE_GEOJSON';

    -- Limpiar tabla temporal
    DROP TABLE IF EXISTS astar_route;
"

echo "GeoJSON con ruta generada en $METRO_ASTAR_ROUTE_GEOJSON"
