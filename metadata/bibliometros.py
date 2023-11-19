import json

# Datos proporcionados
datos_estaciones = [
    {"Estacion": "bellavista", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "irarrazaval", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "san pablo", "Lineas": ["L2", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "plaza de armas", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "quinta normal", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "la cisterna", "Lineas": ["L2", "L4A"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "escuela militar", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "franklin", "Lineas": ["L2", "L6"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "puente alto", "Lineas": ["L4"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "tobalaba", "Lineas": ["L1", "L4"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "vespucio norte", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "los heroes", "Lineas": ["L1", "L2"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "macul", "Lineas": ["L4"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "pajaritos", "Lineas": ["L1"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "baquedano", "Lineas": ["L1", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "los dominicos", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "ciudad del nino", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "plaza egana", "Lineas": ["L3", "L4"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "maipu", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "cerrillos", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"},
    {"Estacion": "lo valledor", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"},
    {"Estacion": "nunoa", "Lineas": ["L3", "L6"], "Ubicacion": "dentro", "Tipo": "expendedor"},
    {"Estacion": "ines de suarez", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"}
]


# Convertir la lista de diccionarios a formato JSON
json_estaciones = json.dumps(datos_estaciones, indent=2)

# Escribir el JSON en un archivo
nombre_archivo = "bibliometros.json"
with open(nombre_archivo, "w") as archivo:
    archivo.write(json_estaciones)

print(f"Se ha creado el archivo JSON: {nombre_archivo}")
