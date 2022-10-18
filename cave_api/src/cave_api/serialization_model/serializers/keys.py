import pkg_resources
data_location = pkg_resources.resource_filename("cave_api", "serialization_model/data/")

specified_keys = {
    'nodes': {
        'required_keys': ['type', 'latitude', 'longitude'],
        'optional_keys': ['altitude']
        },
    'arcs': {
        'required_keys': ['type', 'startLatitude', 'startLongitude', 'endLatitude', 'endLongitude'],
        'optional_keys': ['startAltitude', 'endAltitude', 'startClick', 'endClick', 'height', 'lineBy', 'path']
    },
    'geos': {
        'required_keys': ['type'],
        'optional_keys': ['geoJsonValue']
    }
}
