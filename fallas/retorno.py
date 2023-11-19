import json

# Datos proporcionados
datos_estaciones = [
    {"Estacion": "bellavista", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.46},
    {"Estacion": "irarrazaval", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.6},
    {"Estacion": "san_pablo", "Lineas": ["L2", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.3},
    {"Estacion": "plaza_de_armas", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.15},
    {"Estacion": "quinta_normal", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.34},
    {"Estacion": "la_cisterna", "Lineas": ["L2", "L4A"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.5},
    {"Estacion": "escuela_militar", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.75},
    {"Estacion": "franklin", "Lineas": ["L2", "L6"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.23},
    {"Estacion": "puente_alto", "Lineas": ["L4"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.42},
    {"Estacion": "tobalaba", "Lineas": ["L1", "L4"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.72},
    {"Estacion": "vespucio_norte", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.57},
    {"Estacion": "los_heroes", "Lineas": ["L1", "L2"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.68},
    {"Estacion": "macul", "Lineas": ["L4"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.63},
    {"Estacion": "pajaritos", "Lineas": ["L1"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.37},
    {"Estacion": "baquedano", "Lineas": ["L1", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.43},
    {"Estacion": "los_dominicos", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.8},
    {"Estacion": "ciudad_del_nino", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.51},
    {"Estacion": "plaza_egana", "Lineas": ["L3", "L4"], "Ubicacion": "dentro", "Tipo": "kiosco", "retorno": 0.82},
    {"Estacion": "maipu", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco", "retorno": 0.47},
    {"Estacion": "cerrillos", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor", "retorno": 1},
    {"Estacion": "lo_valledor", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor", "retorno": 1},
    {"Estacion": "nunoa", "Lineas": ["L3", "L6"], "Ubicacion": "dentro", "Tipo": "expendedor", "retorno": 1},
    {"Estacion": "ines_de_suarez", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor", "retorno": 1}
]


# Convertir la lista de diccionarios a formato JSON
json_estaciones = json.dumps(datos_estaciones, indent=2)

# Escribir el JSON en un archivo
nombre_archivo = "retorno.json"
with open(nombre_archivo, "w") as archivo:
    archivo.write(json_estaciones)

print(f"Se ha creado el archivo JSON: {nombre_archivo}")
