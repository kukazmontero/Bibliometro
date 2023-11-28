import psycopg2
from flask import Flask
import json

# Conectarse a BD 
try:
    conn = psycopg2.connect(host="postgis", dbname="metro_santiago_3", user="user", password="password")  
    print("Conexión establecida")

    cur = conn.cursor()

    cur.execute("SELECT 1") 
    print("Ejecutó query OK")

except Exception as e:
    print("Error conectando a PostgreSQL", e)

# Consultar datos 
try:
    cur.execute("SELECT * FROM vista_coordenadas LIMIT 1") 
    rows = cur.fetchall()
    print("Consulta exitosa")

except Exception as e:
    print("Error consultando estaciones", e)

features = []

# Convertir a GeoJSON
for row in rows:
    features.append(
        {"geometry": json.loads(row[1]), 
         "type": "Feature",  
         "properties": {"nombre": row[0]}
        }) 

print(features) 

# Cerrar conexiones
cur.close()  
conn.close()

app = Flask(__name__)

@app.route('/')
def map():
  # Retorna vista mapa
  return "Mapa de estaciones"  

if __name__ == '__main__':
  app.run(debug=True, port=5000, host='0.0.0.0')