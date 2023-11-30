# Importar bibliotecas necesarias
import os
import requests
from bs4 import BeautifulSoup

# Crear directorio 'results' si no existe
directorio_salida = 'results'
if not os.path.exists(directorio_salida):
    os.makedirs(directorio_salida)

# Eliminar todos los archivos que comienzan con 'output' en el directorio 'results'
for nombre_archivo in os.listdir(directorio_salida):
    if nombre_archivo.startswith("output"):
        os.remove(os.path.join(directorio_salida, nombre_archivo))

# URL del sitio web objetivo
url_busqueda = "https://bibliometro.cl/wp-content/themes/bibliometro/ajax/search_book.php"
url_base = "https://bibliometro.cl/libros/"

# Recorrer un rango de valores para el parámetro 's' (4 caracteres)
for i in range(ord('a'), ord('z')+1):
    for j in range(ord('a'), ord('z')+1):
        for k in range(ord('a'), ord('z')+1):
            for l in range(ord('a'), ord('z')+1):
                # Construir el valor para el parámetro 's'
                valor_s = chr(i) + chr(j) + chr(k) + chr(l)

                # Configurar los datos del formulario para la búsqueda
                datos_formulario = {
                    's': valor_s
                    # Agregar otros parámetros de datos del formulario si es necesario
                }

                # Realizar una solicitud POST para buscar libros utilizando los datos del formulario
                respuesta_busqueda = requests.post(url_busqueda, data=datos_formulario)

                # Verificar si la solicitud de búsqueda fue exitosa (código de estado 200)
                if respuesta_busqueda.status_code == 200:
                    # Analizar el contenido HTML utilizando BeautifulSoup
                    sopa_busqueda = BeautifulSoup(respuesta_busqueda.text, 'html.parser')

                    # Extraer el contenido de texto de cada elemento <div>
                    elementos_div = sopa_busqueda.find_all('div')
                    if elementos_div:
                        # Guardar el contenido de texto interno en un archivo de texto sin etiquetas y líneas vacías
                        nombre_archivo = f"output_s_{valor_s}.txt"
                        ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
                        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                            for elemento_div in elementos_div:
                                texto_interno = elemento_div.get_text().strip() + ","

                                # Eliminar líneas que comienzan con "Título "
                                texto_interno = texto_interno.replace("Título ", "")

                                # Reemplazar "/" con una coma
                                texto_interno = texto_interno.replace("/", ",")

                                # Realizar una solicitud GET a https://bibliometro.cl/libros/aaaa
                                url_libro = f"{url_base}{valor_s}"
                                respuesta_libro = requests.get(url_libro)

                                # Verificar si la solicitud de la página del libro fue exitosa (código de estado 200)
                                if respuesta_libro.status_code == 200:
                                    # Verificar si la respuesta contiene la frase "no tiene copias"
                                    contiene_frase = "no tiene copias" in respuesta_libro.text
                                    archivo.write(f"{texto_interno}{'1' if contiene_frase else '0'}\n")
                                    print(f"Datos para s={valor_s} guardados en {ruta_archivo}")
                                else:
                                    print(f"Error para s={valor_s}. Fallo en la solicitud de la página del libro. Código de estado: {respuesta_libro.status_code}")
                                    # Escribir de todas formas
                                    contiene_frase = False
                                    archivo.write(f"{texto_interno}{'1' if contiene_frase else '0'}\n")
                                    print(f"Datos para s={valor_s} guardados en {ruta_archivo}")
                    else:
                        print(f"No se encontraron elementos <div> para s={valor_s}")
                else:
                    print(f"Error para s={valor_s}. Fallo en la solicitud de búsqueda. Código de estado: {respuesta_busqueda.status_code}")

# Fin del código
