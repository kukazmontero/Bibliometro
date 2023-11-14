from flask import Flask, render_template, request
import sqlite3
import heapq

app = Flask(__name__, template_folder='/app/app/templates')

# Ruta para seleccionar estaciones de origen y destino
@app.route('/seleccionar-recorrido', methods=['GET', 'POST'])
def seleccionar_recorrido():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']

        # Consultar el recorrido entre las estaciones
        recorrido = obtener_recorrido(origen, destino)

        return render_template('recorrido.html', recorrido=recorrido)

    # Obtener la lista de estaciones para mostrar en el formulario
    estaciones = obtener_lista_estaciones()
    return render_template('seleccionar_recorrido.html', estaciones=estaciones)

def obtener_recorrido(origen, destino):
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()

    # Consultar el recorrido utilizando una búsqueda en profundidad (DFS)
    cursor.execute('''
        WITH RECURSIVE Recorrido AS (
            SELECT estacion_destino_id, estacion_origen_id
            FROM conexiones
            WHERE estacion_destino_id = ?  -- Iniciar desde la estación de destino
            UNION
            SELECT c.estacion_destino_id, c.estacion_origen_id
            FROM conexiones c
            JOIN Recorrido r ON c.estacion_destino_id = r.estacion_origen_id
        )
        SELECT r.estacion_origen_id, e.nombre
        FROM Recorrido r
        JOIN estaciones e ON r.estacion_origen_id = e.id
        ORDER BY r.estacion_origen_id;
    ''', (obtener_id_estacion(destino),))

    recorrido = cursor.fetchall()

    # Imprime el recorrido obtenido para depuración
    print(f"Recorrido obtenido: {recorrido}")

    conn.close()

    return recorrido

# Función para obtener el ID de una estación por su nombre
def obtener_id_estacion(nombre):
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM estaciones WHERE nombre = ?;', (nombre,))
    id_estacion = cursor.fetchone()[0]

    conn.close()

    return id_estacion

# Función para obtener la lista de estaciones
def obtener_lista_estaciones():
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre FROM estaciones ORDER BY id;')
    estaciones = [row[0] for row in cursor.fetchall()]

    conn.close()

    return estaciones

# Ruta para seleccionar estaciones de origen y destino
@app.route('/seleccionar-ruta', methods=['GET', 'POST'])
def seleccionar_ruta():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']

        # Calcular la ruta utilizando el algoritmo de Dijkstra
        ruta = calcular_ruta(origen, destino)

        return render_template('ruta.html', ruta=ruta)

    # Obtener la lista de estaciones para mostrar en el formulario
    estaciones = obtener_lista_estaciones()
    return render_template('seleccionar_ruta.html', estaciones=estaciones)

def calcular_ruta(origen, destino):
    conn = sqlite3.connect('tu_base_de_datos.db')
    cursor = conn.cursor()

    # Obtener el ID de las estaciones de origen y destino
    id_origen = obtener_id_estacion(origen)
    id_destino = obtener_id_estacion(destino)

    # Obtener la lista de conexiones para construir el grafo
    cursor.execute('''
        SELECT estacion_origen_id, estacion_destino_id, linea
        FROM conexiones
        WHERE estacion_destino_id = ?  -- Iniciar desde la estación de destino
        UNION
        SELECT c.estacion_destino_id, c.estacion_origen_id, c.linea
        FROM conexiones c
        JOIN Recorrido r ON c.estacion_destino_id = r.estacion_origen_id
        ORDER BY estacion_origen_id;
    ''', (obtener_id_estacion(origen),))
    conexiones = cursor.fetchall()

    # Construir el grafo como una lista de tuplas
    grafo = []
    for conexion in conexiones:
        estacion_origen, estacion_destino, linea = conexion
        grafo.append((estacion_origen, estacion_destino, linea))

    # Implementar el algoritmo de Dijkstra
    distancia = {estacion: {'distancia': float('inf'), 'anterior': None} for estacion in grafo}
    distancia[id_origen]['distancia'] = 0
    cola_prioridad = [(0, id_origen)]

    while cola_prioridad:
        actual_distancia, actual_estacion = heapq.heappop(cola_prioridad)

        if actual_distancia > distancia[actual_estacion]['distancia']:
            continue



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

