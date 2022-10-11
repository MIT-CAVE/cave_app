import pkg_resources
from cave_api.serialization_model.serializers import (
    get_categories_data,
    get_app_bar_data,
    get_map_data,
)

from pprint import pp as print


data_location = pkg_resources.resource_filename("cave_api", "serialization_model/data/")

# print(get_categories_data(data_location+'categories/'))
# print(get_app_bar_data(data_location+'appBar/'))
print(get_map_data(data_location+'map/'))
