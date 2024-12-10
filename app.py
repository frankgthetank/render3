import geopandas as gpd
from dash import Dash, html
import dash_leaflet as dl
import json
import requests
from io import BytesIO

# Leer el archivo .gpkg
def load_data(gpkg_path, layer_name=None):
    """
    Carga datos de un archivo .gpkg y devuelve un GeoJSON.
    """
    gdf = gpd.read_file(gpkg_path, layer=layer_name)
    gdf = gdf.to_crs(epsg=4326)  # Convertir a WGS84 (CRS compatible con Leaflet)
    return json.loads(gdf.to_json())

# Ruta al archivo .gpkg


# Cargar el archivo desde una URL
url = "https://drive.google.com/file/d/1yqpCMFVBI7vDbGo-ctzwU2X4EdcR6QiZ/view?usp=sharing"
response = requests.get(url)
with BytesIO(response.content) as f:
    gdf = gpd.read_file(f)

# Convertir a GeoJSON
geo_data = gdf.to_crs(epsg=4326).to_json()





##gpkg_path = "sectores_anonimizados 1.gpkg"  # Coloca el archivo en una carpeta llamada "data"
geojson_data = load_data(geo_data)

# Crear la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),  # Capa base
        dl.GeoJSON(data=geojson_data,  # GeoJSON cargado
                   options={"style": {"color": "blue", "weight": 2}},
                   id="geojson-layer"),
    ], style={'width': '100%', 'height': '500px'}, center=(0, 0), zoom=2)
])

# Servidor para Render
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
