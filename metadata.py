import json
import traceback

def create_table_if_not_exists(file, table_name, columns, primary_key=None):
    if primary_key:
        file.write(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)}, PRIMARY KEY ({', '.join(primary_key)}));\n")
    else:
        file.write(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});\n")

def insert_data_into_bibliometros(file, estacion, lineas, ubicacion, tipo):
    for linea in lineas:
        # Escapar el nombre de la estación para evitar problemas con caracteres especiales
        estacion_escaped = estacion.replace("'", "''")
        file.write(
            f"INSERT INTO bibliometros (estacion, linea, ubicacion, tipo) VALUES ('{estacion_escaped}', '{linea}', '{ubicacion}', '{tipo}');\n"
        )

def insert_data_into_conexiones(file, estacion_origen, estacion_destino, estado):
    # Eliminar apóstrofes de los nombres de las estaciones
    estacion_origen = estacion_origen.replace("'", "")

    # Verificar si estacion_destino es None
    if estacion_destino is not None:
        estacion_destino = estacion_destino.replace("'", "")
    
    file.write(
        f"INSERT INTO conexiones (estacion_origen, estacion_destino, estado) VALUES ('{estacion_origen}', '{estacion_destino}', {estado}) ON CONFLICT (estacion_origen, estacion_destino) DO NOTHING;\n"
    )

def insert_data_into_lineas_estacion(file, estacion_origen, lineas):
    for linea in lineas:
        # Escapar el nombre de la estación para evitar problemas con caracteres especiales
        estacion_origen_escaped = estacion_origen.replace("'", "''")
        file.write(
            f"INSERT INTO lineas_estacion (estacion, linea) VALUES ('{estacion_origen_escaped}', '{linea}');\n"
        )

def insert_data_into_coordenadas(file, estacion, longitud, latitud, estaciones_procesadas):
    # Escapar el nombre de la estación para evitar problemas con caracteres especiales
    estacion_escaped = estacion.replace("'", "")
    
    # Verificar si la estación ya fue procesada
    if estacion_escaped not in estaciones_procesadas:
        file.write(
            f"INSERT INTO coordenadas (estacion, longitud, latitud) VALUES ('{estacion_escaped}', {longitud}, {latitud});\n"
        )

        # Agregar la estación al conjunto de estaciones procesadas
        estaciones_procesadas.add(estacion_escaped)

def insert_data_into_fallas(file, estacion, lineas, ubicacion, tipo, valor, table_name):
    for linea in lineas:
        # Escapar el nombre de la estación para evitar problemas con caracteres especiales
        estacion_escaped = estacion.replace("'", "''")
        file.write(
            f"INSERT INTO {table_name} (estacion, linea, ubicacion, tipo, valor) VALUES ('{estacion_escaped}', '{linea}', '{ubicacion}', '{tipo}', {valor});\n"
        )

def main():
    try:
        # Arreglo para almacenar las estaciones ya procesadas en coordenadas
        estaciones_procesadas = set()

        with open("init.sql", "w", encoding="utf-8") as sql_file:

            sql_file.write(f"CREATE EXTENSION IF NOT EXISTS postgis;\n")
            sql_file.write(f"CREATE EXTENSION IF NOT EXISTS pgrouting;\n")

            # Crear tabla bibliometros
            create_table_if_not_exists(
                sql_file,
                "bibliometros",
                ["estacion TEXT NOT NULL", "ubicacion TEXT", "tipo TEXT", "linea TEXT NOT NULL"],
                primary_key=["estacion", "linea"]
            )

            # Carga e inserción de datos en bibliometros
            with open("metadata/bibliometros.json", "r") as archivo_ubicaciones:
                bibliometros = json.load(archivo_ubicaciones)
                for item in bibliometros:
                    estacion = item.get('Estacion', '')
                    lineas = item.get('Lineas', [])
                    ubicacion = item.get('Ubicacion', '')
                    tipo = item.get('Tipo', '')

                    insert_data_into_bibliometros(sql_file, estacion, lineas, ubicacion, tipo)

            archivo_ubicaciones.close()
            # - - -

            # Crear tabla conexiones
            create_table_if_not_exists(
                sql_file,
                "conexiones",
                ["estacion_origen TEXT NOT NULL", "estacion_destino TEXT", "estado INTEGER NOT NULL"],
                primary_key=["estacion_origen", "estacion_destino"]
            )

            # Cargar datos de conexiones.json
            with open("metadata/conexiones.json", "r") as archivo_conexiones:
                conexiones = json.load(archivo_conexiones)
                for item in conexiones:
                    estacion_origen = item['estacion']
                    estacion_destino = item.get('siguiente estacion')
                    estado = item['estado']

                    # Insertar en la tabla conexiones
                    insert_data_into_conexiones(sql_file, estacion_origen, estacion_destino, estado)

            archivo_conexiones.close()

            # Crear tabla lineas_estacion
            create_table_if_not_exists(
                sql_file,
                "lineas_estacion",
                ["estacion TEXT NOT NULL", "linea TEXT NOT NULL"],
                primary_key=None  # Eliminar la restricción PRIMARY KEY
            )

            # Cargar datos de conexiones.json para la tabla lineas_estacion
            with open("metadata/conexiones.json", "r") as archivo_conexiones:
                conexiones = json.load(archivo_conexiones)
                for item in conexiones:
                    estacion_origen = item['estacion']
                    lineas = item['lineas']

                    # Insertar en la tabla lineas_estacion
                    insert_data_into_lineas_estacion(sql_file, estacion_origen, lineas)

            archivo_conexiones.close()

            # Crear tabla coordenadas
            create_table_if_not_exists(
                sql_file,
                "coordenadas",
                ["estacion TEXT NOT NULL", "longitud REAL NOT NULL", "latitud REAL NOT NULL"],
                primary_key=["estacion"]
            )

            # Carga e inserción de datos en coordenadas
            with open("metadata/ubicacion.json", "r") as archivo_coordenadas:
                coordenadas = json.load(archivo_coordenadas)
                for item in coordenadas:
                    estacion = item['estacion']
                    longitud = item['longitud']
                    latitud = item['latitud']

                    # Insertar en la tabla coordenadas
                    insert_data_into_coordenadas(sql_file, estacion, longitud, latitud, estaciones_procesadas)

            archivo_coordenadas.close()

            # Crear extensiones
            sql_file.write(f"CREATE EXTENSION IF NOT EXISTS postgis;\n")
            sql_file.write(f"CREATE EXTENSION IF NOT EXISTS pgrouting;\n")

            # Crear tablas
            sql_file.write("CREATE TABLE IF NOT EXISTS vertices AS\n")
            sql_file.write("SELECT row_number() OVER () AS id, estacion, longitud, latitud\n")
            sql_file.write("FROM coordenadas;\n")

            sql_file.write("CREATE TABLE conexiones_edges AS\n")
            sql_file.write("SELECT\n")
            sql_file.write("    e.id,\n")
            sql_file.write("    v1.id AS source,\n")
            sql_file.write("    v2.id AS target,\n")
            sql_file.write("    e.estado AS cost\n")
            sql_file.write("FROM\n")
            sql_file.write("    conexiones e\n")
            sql_file.write("    JOIN vertices v1 ON e.estacion_origen = v1.estacion\n")
            sql_file.write("    JOIN vertices v2 ON e.estacion_destino = v2.estacion;\n")

            # Realizar la consulta
            sql_file.write("SELECT pgr_createTopology('conexiones_edges', 0.0001, 'source', 'target', 'id');\n")
            sql_file.write("SELECT seq, node, edge, cost, agg_cost, geom\n")
            sql_file.write("FROM pgr_dijkstra(\n")
            sql_file.write("    'SELECT id, source, target, cost FROM conexiones_edges',\n")
            sql_file.write("    (SELECT id FROM conexiones_edges WHERE source = (SELECT id FROM vertices WHERE estacion = 'Estacion_Origen')),\n")
            sql_file.write("    (SELECT id FROM conexiones_edges WHERE target = (SELECT id FROM vertices WHERE estacion = 'Estacion_Destino')),\n")
            sql_file.write("    directed := true\n")
            sql_file.write(") AS di\n")
            sql_file.write("JOIN coordenadas AS c ON di.node = c.id;\n")

            # Crear tabla para bestsellers_espanol.json
            create_table_if_not_exists(
                sql_file,
                "bestsellers_espanol",
                ["titulo TEXT NOT NULL", "autos INTEGER NOT NULL"],
                primary_key=["titulo"]
            )

            # Cargar datos de bestsellers_espanol.json
            with open("fallas/bestsellers_espanol.json", "r", encoding="utf-8") as archivo_bestsellers:

                bestsellers = json.load(archivo_bestsellers)
                for item in bestsellers:
                    titulo = item.get('titulo', '')
                    autos = item.get('autos', 0)

                    # Insertar en la tabla bestsellers_espanol
                    insert_data_into_fallas(sql_file, titulo, [], '', '', autos, 'bestsellers_espanol')

            archivo_bestsellers.close()

            # Crear tabla para retorno.json
            create_table_if_not_exists(
                sql_file,
                "retorno",
                ["estacion TEXT NOT NULL", "lineas TEXT[] NOT NULL", "ubicacion TEXT NOT NULL", "tipo TEXT NOT NULL", "retorno REAL NOT NULL"],
                primary_key=["estacion"]
            )

            # Cargar datos de retorno.json
            with open("fallas/retorno.json", "r", encoding="utf-8") as archivo_retorno:
                retorno = json.load(archivo_retorno)
                for item in retorno:
                    estacion = item.get('Estacion', '')
                    lineas = item.get('Lineas', [])
                    ubicacion = item.get('Ubicacion', '')
                    tipo = item.get('Tipo', '')
                    retorno_valor = item.get('retorno', 0.0)

                    # Insertar en la tabla retorno
                    insert_data_into_fallas(sql_file, estacion, lineas, ubicacion, tipo, retorno_valor, 'retorno')

            archivo_retorno.close()

            # Crear tabla para trabajador.json
            create_table_if_not_exists(
                sql_file,
                "trabajador",
                ["estacion TEXT NOT NULL", "lineas TEXT[] NOT NULL", "ubicacion TEXT NOT NULL", "tipo TEXT NOT NULL", "trabajador REAL NOT NULL"],
                primary_key=["estacion"]
            )

            # Cargar datos de trabajador.json
            with open("fallas/trabajador.json", "r", encoding="utf-8") as archivo_trabajador:
                trabajador = json.load(archivo_trabajador)
                for item in trabajador:
                    estacion = item.get('Estacion', '')
                    lineas = item.get('Lineas', [])
                    ubicacion = item.get('Ubicacion', '')
                    tipo = item.get('Tipo', '')
                    trabajador_valor = item.get('Trabajador', 0.0)

                    # Insertar en la tabla trabajador
                    insert_data_into_fallas(sql_file, estacion, lineas, ubicacion, tipo, trabajador_valor, 'trabajador')

            archivo_trabajador.close()

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
