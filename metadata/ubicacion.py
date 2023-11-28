import pandas as pd
import json
import unicodedata

# Función para quitar tildes y reemplazar "ñ" por "n"
def limpiar_texto(texto):
    texto_sin_tilde = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return texto_sin_tilde.replace('ñ', 'n').replace('Ñ', 'N')

# Lee el archivo Excel
df = pd.read_excel('metro_20231115_-oficio-4770_2013.xlsx')

# Modifica el DataFrame para convertir los nombres a minúsculas, eliminar espacios al final y aplicar el filtro de caracteres especiales
df['estacion'] = df['estacion'].apply(lambda x: limpiar_texto(str(x).lower().strip()))

# Convierte el DataFrame a un diccionario y luego a formato JSON
data_dict = df.to_dict(orient='records')

# Guarda el resultado en un archivo JSON
with open('ubicacion.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=2)
