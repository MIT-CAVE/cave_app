import json
import pkg_resources
from cave_api.serialization_model.serializers import (
    get_categories_data,
    get_app_bar_data,
    get_map_data,
    get_data
)

data_location = pkg_resources.resource_filename("cave_api", "serialization_model/data/")

def get_api_object():
    with open(data_location+'settings.json') as f: settings = json.load(f)
    with open(data_location+'stats.json') as f: stats = json.load(f)
    with open(data_location+'kpis.json') as f: kpis = json.load(f)
    with open(data_location+'kwargs.json') as f: kwargs = json.load(f)
    example = {
        'settings':settings,
        'categories':get_categories_data(data_location+'categories/'),
        'appBar':get_app_bar_data(data_location+'appBar/'),
        'map':get_map_data(data_location+'map/'),
        'arcs':get_data(data_location+'arcs/'),
        'nodes':get_data(data_location+'nodes/'),
        'geos':get_data(data_location+'geos/'),
        'stats':stats,
        'kpis':kpis,
        'kwargs':kwargs
    }
    return example
