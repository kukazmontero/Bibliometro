import sqlite3
import requests


def create_or_update_tables(conn):
    cursor = conn.cursor()

    # Crear la tabla estaciones si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estaciones (
            id INTEGER PRIMARY KEY,
            nombre TEXT UNIQUE,
            hora_apertura TEXT,
            hora_cierre TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estaciones_lineas (
            id INTEGER PRIMARY KEY,
            estacion_id INTEGER,
            linea TEXT,
            FOREIGN KEY (estacion_id) REFERENCES estaciones (id)
        );
    ''')

    # Crear la tabla conexiones si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conexiones (
            id INTEGER PRIMARY KEY,
            estacion_origen_id INTEGER,
            estacion_destino_id INTEGER,
            linea TEXT,  -- Nueva columna para almacenar la línea
            FOREIGN KEY (estacion_origen_id) REFERENCES estaciones (id),
            FOREIGN KEY (estacion_destino_id) REFERENCES estaciones (id)
        );
    ''')

    # Guardar los cambios
    conn.commit()

def insert_or_replace_station(conn, station_name, open_time, close_time, lines):
    cursor = conn.cursor()

    # Asegúrate de que open_time y close_time sean strings
    open_time_str = str(open_time)
    close_time_str = str(close_time)

    # Insertar o actualizar la estación en la tabla estaciones
    cursor.execute("INSERT OR REPLACE INTO estaciones (nombre, hora_apertura, hora_cierre) VALUES (?, ?, ?);", (station_name, open_time_str, close_time_str))

    # Obtener el ID de la estación
    estacion_id = obtener_id_estacion(conn, station_name)

    # Eliminar las líneas antiguas asociadas a la estación
    cursor.execute("DELETE FROM estaciones_lineas WHERE estacion_id = ?;", (estacion_id,))

    # Insertar las nuevas líneas asociadas a la estación
    for line in lines:
        cursor.execute("INSERT INTO estaciones_lineas (estacion_id, linea) VALUES (?, ?);", (estacion_id, line))

    # Guardar los cambios
    conn.commit()


def insert_connection(conn, estacion_origen, estacion_destino, linea):
    cursor = conn.cursor()

    # Obtener los IDs de las estaciones o crearlas si no existen
    estacion_origen_id = obtener_id_estacion(conn, estacion_origen)
    estacion_destino_id = obtener_id_estacion(conn, estacion_destino)

    print("test 1 AAAA")

    if estacion_origen_id is None or estacion_destino_id is None:
        # Se produjo un error al obtener o crear las estaciones
        print(f"No se pudo obtener o crear una o ambas estaciones para la conexión: {estacion_origen} -> {estacion_destino}")
        return

    # Insertar la conexión en la tabla conexiones
    cursor.execute("INSERT OR REPLACE INTO conexiones (estacion_origen_id, estacion_destino_id, linea) VALUES (?, ?, ?);", (estacion_origen_id, estacion_destino_id, linea))

    # Guardar los cambios
    conn.commit()

    print(f"Conexión insertada: {estacion_origen} -> {estacion_destino}, Línea: {linea}")

def obtener_id_estacion(conn, nombre_estacion):
    cursor = conn.cursor()

    # Intentar obtener el ID de la estación por su nombre
    cursor.execute("SELECT id FROM estaciones WHERE nombre = ?;", (nombre_estacion,))
    result = cursor.fetchone()

    print("test 1 bbbbb", nombre_estacion,result)

    if result:
        # Si la estación ya existe, retornar su ID
        return result[0]
    else:
        # Si la estación no existe, puedes optar por insertarla y luego obtener su ID
        cursor.execute("INSERT INTO estaciones (nombre) VALUES (?);", (nombre_estacion,))
        conn.commit()
        return cursor.lastrowid


def update_station_lines(conn, station_name, lines):
    cursor = conn.cursor()

    # Obtener el ID de la estación
    estacion_id = obtener_id_estacion(conn, station_name)

    # Eliminar las líneas antiguas asociadas a la estación
    cursor.execute("DELETE FROM estaciones_lineas WHERE estacion_id = ?;", (estacion_id,))

    # Insertar las nuevas líneas asociadas a la estación
    for line in lines:
        cursor.execute("INSERT INTO estaciones_lineas (estacion_id, linea) VALUES (?, ?);", (estacion_id, line))

    # Guardar los cambios
    conn.commit()


def main():
    url = "https://api.xor.cl/red/metro-network"

    response = requests.get(url)

    if response.status_code == 200:
        metro_data = response.json()

        sql_file = "horarios_estaciones.sql"

        with open(sql_file, "w") as file:
            # Conectar a la base de datos (si no existe, la creará)
            conn = sqlite3.connect('tu_base_de_datos.db')

            # Crear o actualizar las tablas
            create_or_update_tables(conn)

            # Iterar sobre las líneas y estaciones para crear las instrucciones SQL
            for line in metro_data["lines"]:
                line_name = line["name"]
                for i, station in enumerate(line["stations"]):
                    station_name = station["name"]
                    open_time = station["schedule"]["open"]
                    close_time = station["schedule"]["close"]

                    # Obtener las líneas asociadas a la estación
                    lines = station.get("lines", [])

                    # Insertar o actualizar la estación en la tabla estaciones
                    insert_or_replace_station(conn, station_name, open_time, close_time, lines)

                    # Escribir en el archivo SQL (opcional)
                    file.write(f"INSERT OR REPLACE INTO estaciones (nombre, hora_apertura, hora_cierre) VALUES ('{station_name}', '{open_time}', '{close_time}');\n")

                    # Agregar conexión si no es la primera estación de la línea
                    if i > 0:
                        estacion_origen = line["stations"][i-1]["name"]
                        insert_connection(conn, estacion_origen, station_name, line_name)

                    # Guardar información sobre las líneas que pasa cada estación
                    update_station_lines(conn, station_name, lines)

            # Cerrar la conexión después de haber terminado de escribir en el archivo
            conn.close()

            print(f"El archivo SQL '{sql_file}' ha sido creado para crear o actualizar las tablas y los datos.")
    else:
        print(f"Error al obtener los datos. Código de respuesta: {response.status_code}")

if __name__ == "__main__":
    main()
