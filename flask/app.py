import time
import psycopg2
from flask import Flask, render_template, send_file 
from flask_socketio import SocketIO
import geopandas as gpd
import sqlalchemy.exc

app = Flask(__name__)
socketio = SocketIO(app)

# Configuración de la conexión a la BD  
db_host = "postgres"
db_name = "metro_santiago_3"
db_user = "user"
db_password = "password"
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

MAX_CONN_ATTEMPTS = 20

def connect_to_db():
    attempt = 0
    while attempt < MAX_CONN_ATTEMPTS:
        try:
            print(f"Intento {attempt+1} de conectarse a BD")
            conn = psycopg2.connect(connection_string) 
            return conn
        except psycopg2.OperationalError as e:
            print(f"Error conectando a BD: {e}")
            attempt += 1
            time.sleep(5)

    print("No se pudo conectar a la BD") 
    sys.exit(1)

conn = connect_to_db()  
print("Conexión exitosa")

def obtener_coordenadas():
    try:
        gdf = gpd.read_postgis("SELECT * FROM coordenadas", connection_string)
        return gdf
    except Exception as e:
        print(f"Error al consultar BD: {e}")
        return None
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa_estaciones') 
def mapa_estaciones():
    return send_file('../output/mapa_estaciones.png', mimetype='image/png')   

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)