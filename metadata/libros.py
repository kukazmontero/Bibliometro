import json
import requests
from bs4 import BeautifulSoup

# Define la URL base del catálogo de Bibliometro
BASE_URL = "https://bibliometro.cl/catalogo/"

# Lista de estaciones de Bibliometro para hacer scraping
ESTACIONES = [
    "Los Libertadores",
    "Universidad de Chile",
    "Baquedano",
    "Bellavista",
    "Ciudad del Niño",
    "Escuela Militar",
    "Franklin",
    "Irarrázaval",
    "La Cisterna",
    "Los Dominicos",
    "Los Héroes",
    "Maipú",
    "Pajaritos",
    "Plaza de Armas",
    "Plaza Egaña",
    "Puente Alto",
    "Quinta Normal",
    "San Pablo",
    "Tobalaba",
    "Vespucio Norte"
]

# Inicializa un diccionario para almacenar los datos
libros_a_estaciones = {}

# Función para hacer scraping de detalles de un libro
def hacer_scraping_detalle_libro(url):
    detalles_libro = {}
    
    # Realiza una solicitud GET a la URL del libro
    response = requests.get(url)
    if response.status_code == 200:
        # Parsea el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encuentra los detalles del libro en el HTML parseado
        # Necesitarás analizar el sitio web y ajustar las siguientes líneas en consecuencia
        autor = soup.find('h4').text.strip() if soup.find('h4') else None
        detalles_libro["autor"] = autor

        # Encuentra el nombre de la(s) estación(es) aquí y ajusta la línea siguiente en consecuencia
        estaciones = [estacion.text.strip() for estacion in soup.find_all('li', class_='location cortar')]
        detalles_libro["estaciones"] = estaciones

        # Puedes agregar más detalles aquí según sea necesario
        
    else:
        print(f"Fallo al recuperar la página del libro con código de estado: {response.status_code}")

    return detalles_libro

# Función para hacer scraping de títulos de libros y estaciones
def hacer_scraping_libros():
    # Realiza una solicitud GET a la URL
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        # Parsea el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encuentra los títulos de los libros y las estaciones en el HTML parseado
        # Necesitarás analizar el sitio web y ajustar las siguientes líneas en consecuencia
        libros = soup.find_all('div', class_='row black-box')  # Esto es un ejemplo; ajústalo según sea necesario
        for libro in libros:
            # Encuentra el título del libro y ajusta según sea necesario
            titulo = libro.find('h3').text.strip()

            # Construye la URL del detalle del libro
            url_detalle_libro = BASE_URL + libro.find('a')['href']

            # Obtén los detalles del libro utilizando la nueva función
            detalles_libro = hacer_scraping_detalle_libro(url_detalle_libro)

            # Manejo de errores para evitar KeyError
            estaciones_libro = detalles_libro.get("estaciones", [])
            
            # Agrega al diccionario, acumulando estaciones para cada libro
            libros_a_estaciones[titulo] = estaciones_libro
    else:
        print(f"Fallo al recuperar la página con código de estado: {response.status_code}")

# Hacer scraping de libros para cada estación
hacer_scraping_libros()

# Convierte nuestro diccionario a JSON y guarda en un archivo
ruta_archivo_json = 'libros.json'
with open(ruta_archivo_json, 'w') as archivo_json:
    json.dump(libros_a_estaciones, archivo_json, ensure_ascii=False, indent=4)
