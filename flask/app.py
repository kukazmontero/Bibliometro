from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
import geopandas as gpd
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


app = Flask(__name__)
socketio = SocketIO(app)

# Conexión a la base de datos PostGIS
connection_string = "postgresql://user:password@postgis:5432/metro_santiago_3"


def wait_for_db():
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Intenta crear una conexión a la base de datos
            engine = create_engine(connection_string)
            engine.connect()
            print("Conexión exitosa a la base de datos")
            return
        except OperationalError as e:
            print(f"Error de conexión a la base de datos: {e}")
            print(f"Intento {retry_count + 1}/{max_retries}. Esperando 20 segundos...")
            retry_count += 1
            time.sleep(20)

    print("No se pudo establecer conexión con la base de datos después de múltiples intentos. Saliendo.")
    exit()


# Función para obtener las coordenadas de la base de datos
def obtener_coordenadas():
    gdf = gpd.read_postgis("SELECT * FROM coordenadas", connection_string)
    return gdf

# Ruta para servir la página web
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para servir el mapa
@app.route('/mapa_estaciones')
def mapa_estaciones():
    return send_file('output/mapa_estaciones.png', mimetype='image/png')

# Función que emite las coordenadas al cliente
def emitir_coordenadas():
    while True:
        gdf = obtener_coordenadas()
        socketio.emit('actualizar_mapa', gdf.to_json(), namespace='/mapa')
        time.sleep(5)

if __name__ == '__main__':
    # Esperar a que la base de datos esté disponible antes de iniciar la aplicación
    if wait_for_db():
        # Iniciar el hilo para emitir coordenadas en segundo plano
        import threading
        thread = threading.Thread(target=emitir_coordenadas)
        thread.start()

        # Iniciar la aplicación Flask con SocketIO
        socketio.run(app, host='0.0.0.0', port=5001)
    else:
        print("La aplicación no puede iniciarse porque no se pudo conectar a la base de datos.")

