# This file requires the use of scgraph
# scgraph can be installed via `pip install scgraph>=2.3.0`
from scgraph.geographs.marnet import marnet_geograph
from scgraph.core import get_multi_path_geojson

# Define the routes to calculate for the GeoJSON file
routes = [
    {
        "properties":{"id": "Baltimore-London"}, 
        "origin":{"latitude":39.2904, "longitude":-76.6122}, 
        "destination":{"latitude":51.5074, "longitude":-0.1278},
        "geograph": marnet_geograph
    },
    {
        "properties":{"id": "Baltimore-Paris"}, 
        "origin":{"latitude":39.2904, "longitude":-76.6122}, 
        "destination":{"latitude":48.8566, "longitude":2.3522},
        "geograph": marnet_geograph
    },
    {
        "properties":{"id": "Baltimore-Berlin"}, 
        "origin":{"latitude":39.2904, "longitude":-76.6122}, 
        "destination":{"latitude":52.5200, "longitude":13.4050},
        "geograph": marnet_geograph
    },
]

# Create the GeoJSON file
get_multi_path_geojson(
    routes=routes, 
    filename="multi_route.geojson",
    show_progress=True
)
print("GeoJSON file created successfully!")