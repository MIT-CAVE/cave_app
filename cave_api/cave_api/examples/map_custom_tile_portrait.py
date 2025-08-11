from cave_utils import CustomCoordinateSystem


def execute_command(session_data, socket, command="init", **kwargs):
    # Create a portrait coordinate system (1:2) based on the dimensions of the background image
    coordinate_system = CustomCoordinateSystem(300, 600)

    # Generate coordinates on intersection points
    width = 8
    height = 15
    square_size = 600 / 14
    coordinates = []
    for x in range(width):
        x_coord = x * square_size
        for y in range(height):
            y_coord = y * square_size
            coordinates.append([x_coord, y_coord])

    # Convert (x,y) coordinates to (lat,long) to properly display the points on the Mercator projection map
    locations_dict = coordinate_system.serialize_nodes(coordinates)

    amounts = [100] * len(coordinates)
    availabilities = [False] * len(coordinates)

    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0",
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": [
                    "mapPage",
                ],
            },
            "data": {
                # Add an appBar button to launch a map focused dashboard
                "mapPage": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "upperLeft",
                },
            },
        },
        "maps": {
            # Specify the order of map style items as they will appear in the style selector
            "order": {
                "additionalMapStyles": ["grid"],
            },
            # Add custom map styles
            "additionalMapStyles": {
                "grid": {
                    "name": "Grid",
                    "icon": "md/MdBrush",
                    # See the `style` key in the following mapbox gl reference spec:
                    # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                    "spec": {
                        "version": 8,
                        "sources": {
                            "grid": {
                                "type": "raster",
                                "tiles": [
                                    "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/refs/heads/main/example_data/portrait_grid_tiles/{z}/{x}/{y}.png"
                                ],
                                "tileSize": 256,
                                "attribution": "Map tiles by <a target='_top' rel='noopener' href='https://osmfoundation.org/'>OpenStreetMap</a>, under <a target='_top' rel='noopener' href='https://osmfoundation.org/copyright'>Open Database License</a>.",
                            },
                        },
                        "layers": [
                            {
                                "id": "simple-tiles",
                                "type": "raster",
                                "source": "grid",
                                "minzoom": 0,
                                "maxzoom": 22,
                            },
                        ],
                    },
                },
            },
            # Specify available map projections that can be selected in the dashboards by the user
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "mercator",
                    # Specify the current style for the map
                    "currentStyle": "grid",
                    # Specify the default viewport for the map
                    "defaultViewport": {
                        "longitude": 0,
                        "latitude": 0,
                        "zoom": 0,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 0,
                    },
                    "legendGroups": {
                        "items": {
                            "name": "Items",
                            "data": {
                                "point": {
                                    "value": True,
                                    "colorBy": "availability",
                                    "colorByOptions": [
                                        "amount",
                                        "availability",
                                    ],
                                    "sizeBy": "amount",
                                    "sizeByOptions": ["amount"],
                                    "icon": "fa/FaCircle",
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "point": {
                    "type": "node",
                    "name": "Point",
                    "props": {
                        "amount": {
                            "name": "Amount",
                            "type": "num",
                            "unit": "Example Unit",
                            "help": "Example Amount",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": "min",
                                        "size": "35px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": "max",
                                        "size": "45px",
                                        "color": "rgb(96 2 2)",
                                    },
                                ],
                            },
                        },
                        "availability": {
                            "name": "Availability",
                            "type": "toggle",
                            "help": "Whether the space is available",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": locations_dict,
                        "valueLists": {
                            "amount": amounts,
                            "availability": availabilities,
                        },
                    },
                },
            }
        },
        # Add a map page to the app using the example map specified above
        "pages": {
            "currentPage": "mapPage",
            "data": {
                "mapPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "exampleMap",
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
            },
        },
    }
