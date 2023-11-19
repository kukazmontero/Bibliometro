import json
import random

# Datos proporcionados
datos_estaciones = [
    {"Estacion": "bellavista", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "irarrazaval", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "san_pablo", "Lineas": ["L2", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "plaza_de_armas", "Lineas": ["L3", "L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "quinta_normal", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "la_cisterna", "Lineas": ["L2", "L4A"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "escuela_militar", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "franklin", "Lineas": ["L2", "L6"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "puente_alto", "Lineas": ["L4"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "tobalaba", "Lineas": ["L1", "L4"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "vespucio_norte", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "los_heroes", "Lineas": ["L1", "L2"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "macul", "Lineas": ["L4"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "pajaritos", "Lineas": ["L1"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "baquedano", "Lineas": ["L1", "L5"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "los_dominicos", "Lineas": ["L1"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "ciudad_del_nino", "Lineas": ["L2"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "plaza_egana", "Lineas": ["L3", "L4"], "Ubicacion": "dentro", "Tipo": "kiosco"},
    {"Estacion": "maipu", "Lineas": ["L5"], "Ubicacion": "fuera", "Tipo": "kiosco"},
    {"Estacion": "cerrillos", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"},
    {"Estacion": "lo_valledor", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"},
    {"Estacion": "nunoa", "Lineas": ["L3", "L6"], "Ubicacion": "dentro", "Tipo": "expendedor"},
    {"Estacion": "ines_de_suarez", "Lineas": ["L6"], "Ubicacion": "fuera", "Tipo": "expendedor"},
]

# Agregar la columna "trabajador"
for estacion in datos_estaciones:
    if estacion["Tipo"] == "expendedor":
        estacion["Trabajador"] = 1
    else:
        estacion["Trabajador"] = random.uniform(0.5, 1)

# Convertir la lista de diccionarios a formato JSON
json_estaciones = json.dumps(datos_estaciones, indent=2)

# Escribir el JSON en un archivo
nombre_archivo = "trabajador.json"
with open(nombre_archivo, "w") as archivo:
    archivo.write(json_estaciones)

print(f"Se ha creado el archivo JSON: {nombre_archivo}")
