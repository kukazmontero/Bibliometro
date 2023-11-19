import pandas as pd
import json

# Lee el archivo Excel
df = pd.read_excel('metro_20231115_-oficio-4770_2013.xlsx')

# Modifica el DataFrame para convertir los nombres a minúsculas y eliminar espacios al final
df['estacion'] = df['estacion'].str.lower().str.strip()

# Convierte el DataFrame a un diccionario y luego a formato JSON
data_dict = df.to_dict(orient='records')

# Guarda el resultado en un archivo JSON
with open('ubicacion.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=2)
