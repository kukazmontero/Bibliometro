import requests
import json

def obtener_bestsellers_espanol():
    url = "https://api.bookreads.dev/bestsellers-spanish"

    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()

        bestsellers_espanol = []
        
        for fecha, libros in datos.items():
            for libro in libros:
                titulo = libro.get('title', 'Sin título')
                autor = libro.get('author', 'Autor desconocido')
                
                libro_espanol = {
                    'titulo': titulo,
                    'autor': autor
                }

                bestsellers_espanol.append(libro_espanol)

        # Guardar la información en un archivo JSON
        with open('bestsellers_espanol.json', 'w', encoding='utf-8') as archivo:
            json.dump(bestsellers_espanol, archivo, ensure_ascii=False, indent=2)

    else:
        print(f"Error al obtener datos. Código de estado: {respuesta.status_code}")

if __name__ == "__main__":
    obtener_bestsellers_espanol()
