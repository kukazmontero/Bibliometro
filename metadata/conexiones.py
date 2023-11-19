import requests
import json
import unicodedata

# Función para quitar tildes y reemplazar "ñ" por "n"
def limpiar_texto(texto):
    texto_sin_tilde = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return texto_sin_tilde.replace('ñ', 'n').replace('Ñ', 'N')

# URL de la API
url = "https://api.xor.cl/red/metro-network"

# Realizar la solicitud GET a la API
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertir la respuesta JSON en un objeto Python
    data = response.json()

    # Lista para almacenar la información de las estaciones
    estaciones_info = []

    # Función para procesar la información de las estaciones
    def procesar_estaciones(linea):
        for estacion in linea["stations"]:
            nombre_estacion_original = estacion["name"]
            nombre_estacion = limpiar_texto(nombre_estacion_original.lower())
            lineas_correspondientes = estacion["lines"]
            estado_estacion = estacion["status"]
            estacion_continua = None

            # Encontrar la estación continua si existe
            if estacion["status"] == 0:  # Estación operativa
                index_actual = linea["stations"].index(estacion)
                if index_actual < len(linea["stations"]) - 1:
                    estacion_continua = limpiar_texto(linea["stations"][index_actual + 1]["name"].lower())

            # Agregar la información a la lista
            estacion_info = {
                "estacion": nombre_estacion,
                "lineas": lineas_correspondientes,
                "estado": estado_estacion,
                "siguiente estacion": estacion_continua
            }
            estaciones_info.append(estacion_info)

    # Procesar cada línea
    for linea in data["lines"]:
        procesar_estaciones(linea)

    # Escribir la información en un archivo JSON
    with open("conexiones.json", "w", encoding="utf-8") as json_file:
        json.dump(estaciones_info, json_file, indent=2, ensure_ascii=False)

    print("La información ha sido exportada correctamente a conexiones.json")
else:
    # Imprimir un mensaje de error si la solicitud no fue exitosa
    print(f"Error en la solicitud. Código de estado: {response.status_code}")
