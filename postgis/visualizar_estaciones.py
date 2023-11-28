import geopandas as gpd
import matplotlib.pyplot as plt

# Conexión a la base de datos PostGIS
connection_string = "postgresql://user:password@postgres:5432/metro_santiago_3"
gdf = gpd.read_postgis("SELECT * FROM coordenadas", connection_string)

# Imprime el DataFrame para verificar que se cargó correctamente
print("Imprimiendo gdf: ",gdf)

# Crear un mapa
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, marker='o', color='red', markersize=50)
plt.title('Estaciones de Metro Santiago')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.savefig('/output/mapa_estaciones.png')

# Imprime un mensaje para confirmar que se guardó la imagen
print("Mapa guardado en /output/mapa_estaciones.png")
