from cave_utils import CustomCoordinateSystem


def execute_command(session_data, socket, command="init", **kwargs):
    # Create different coordinate systems for each map based on the dimensions of the background image
    square_coordinate_system = CustomCoordinateSystem(600, 600)
    landscape_coordinate_system = CustomCoordinateSystem(600, 300)
    portrait_coordinate_system = CustomCoordinateSystem(300, 600)
    warehouse_coordinate_system = CustomCoordinateSystem(2048, 2048)

    # Generate coordinates on intersection points
    width = height = 15
    square_size = 600 / 14
    square_coordinates = []
    landscape_coordinates = []
    portrait_coordinates = []
    for x in range(width):
        x_coord = x * square_size
        for y in range(height):
            y_coord = y * square_size
            if x < 8:
                portrait_coordinates.append([x_coord, y_coord])
            if y < 8:
                landscape_coordinates.append([x_coord, y_coord])
            square_coordinates.append([x_coord, y_coord])
    
    robot_node_coordinates = [[399, 1798]]
    robot_path_coordinates = [
        [
            [395, 1744],
            [400, 1171],
            [1017, 1171],
            [1026, 524]
        ]
    ]
    region_coordinates = [
        [
            [1400, 1024],
            [2000, 1024],
            [2000, 2000],
            [1400, 2000],
            [1400, 1024]
        ]
    ]

    # Convert (x,y) coordinates to (lat,long) to properly display the points on the Mercator projection map
    square_locations_dict = square_coordinate_system.serialize_nodes(square_coordinates)
    landscape_locations_dict = landscape_coordinate_system.serialize_nodes(landscape_coordinates)
    portrait_locations_dict = portrait_coordinate_system.serialize_nodes(portrait_coordinates)
    robot_node_locations_dict = warehouse_coordinate_system.serialize_nodes(robot_node_coordinates)
    robot_path_locations_dict = warehouse_coordinate_system.serialize_arcs(robot_path_coordinates)
    region_locations_dict = warehouse_coordinate_system.serialize_arcs(region_coordinates)

    # Generate valueLists values
    square_amounts = [100] * len(square_coordinates)
    square_availabilities = [False] * len(square_coordinates)

    landscape_amounts = [100] * len(landscape_coordinates)
    landscape_availabilities = [False] * len(landscape_coordinates)

    portrait_amounts = [100] * len(portrait_coordinates)
    portrait_availabilities = [False] * len(portrait_coordinates)

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
                "additionalMapStyles": ["squareGrid", "landscapeGrid", "portraitGrid", "warehouse"],
            },
            # Add custom map styles
            "additionalMapStyles": {
                "squareGrid": {
                    "name": "Square Grid",
                    "icon": "md/MdBrush",
                    # See the `style` key in the following mapbox gl reference spec:
                    # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                    "spec": {
                        "version": 8,
                        "sources": {
                            "grid": {
                                "type": "raster",
                                "tiles": [
                                    "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/refs/heads/main/example_data/square_grid_tiles/{z}/{x}/{y}.png"
                                ],
                                "tileSize": 256,
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
                "landscapeGrid": {
                    "name": "Landscape Grid",
                    "icon": "md/MdBrush",
                    # See the `style` key in the following mapbox gl reference spec:
                    # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                    "spec": {
                        "version": 8,
                        "sources": {
                            "grid": {
                                "type": "raster",
                                "tiles": [
                                    "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/refs/heads/main/example_data/landscape_grid_tiles/{z}/{x}/{y}.png"
                                ],
                                "tileSize": 256,
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
                "portraitGrid": {
                    "name": "Portrait Grid",
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
                "warehouse": {
                    "name": "Warehouse",
                    "icon": "md/MdBrush",
                    # See the `style` key in the following mapbox gl reference spec:
                    # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                    "spec": {
                        "version": 8,
                        "sources": {
                            "grid": {
                                "type": "raster",
                                "tiles": [
                                    "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/refs/heads/main/example_data/warehouse_grid_tiles/{z}/{x}/{y}.png"
                                ],
                                "tileSize": 512,
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
                "squareMap": {
                    "name": "Square Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "mercator",
                    # Specify the current style for the map
                    "currentStyle": "squareGrid",
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
                            "name": "Points",
                            "data": {
                                "squareGridPoint": {
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
                "landscapeMap": {
                    "name": "Landscape Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "mercator",
                    # Specify the current style for the map
                    "currentStyle": "landscapeGrid",
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
                            "name": "Points",
                            "data": {
                                "landscapeGridPoint": {
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
                "portraitMap": {
                    "name": "Portrait Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "mercator",
                    # Specify the current style for the map
                    "currentStyle": "portraitGrid",
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
                            "name": "Points",
                            "data": {
                                "portraitGridPoint": {
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
                "warehouseMap": {
                    "name": "Warehouse Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "mercator",
                    # Specify the current style for the map
                    "currentStyle": "warehouse",
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
                        "robot": {
                            "name": "Robot",
                            "data": {
                                "robot": {
                                    "value": True,
                                    "colorBy": "availability",
                                    "colorByOptions": [
                                        "amount",
                                        "availability",
                                    ],
                                    "sizeBy": "amount",
                                    "sizeByOptions": ["amount"],
                                    "icon": "fa/FaRobot",
                                },
                                "robotPath": {
                                    "value": True,
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": ["capacity", "preferredRoute"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                },
                            },
                        },
                        "regions": {
                            "name": "Regions",
                            "data": {
                                "region": {
                                    "value": True,
                                    "icon": "bi/BiPolygon",
                                    "colorBy": "isAvailable",
                                    "colorByOptions": ["isAvailable"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "squareGridPoint": {
                    "type": "node",
                    "name": "Square Grid Point",
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
                        "location": square_locations_dict,
                        "valueLists": {
                            "amount": square_amounts,
                            "availability": square_availabilities,
                        },
                    },
                },
                "landscapeGridPoint": {
                    "type": "node",
                    "name": "Landscape Grid Point",
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
                        "location": landscape_locations_dict,
                        "valueLists": {
                            "amount": landscape_amounts,
                            "availability": landscape_availabilities,
                        },
                    },
                },
                "portraitGridPoint": {
                    "type": "node",
                    "name": "Portrait Grid Point",
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
                        "location": portrait_locations_dict,
                        "valueLists": {
                            "amount": portrait_amounts,
                            "availability": portrait_availabilities,
                        },
                    },
                },
                "robot": {
                    "type": "node",
                    "name": "Robot",
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
                                        "size": "50px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": "max",
                                        "size": "100px",
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
                        "location": robot_node_locations_dict,
                        "valueLists": {
                            "amount": [100],
                            "availability": [False],
                        },
                    },
                },
                "robotPath": {
                    "type": "arc",
                    "name": "Robot Path",
                    "props": {
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "unit": "Cubic Feet",
                            "help": "The warehouse capacity in cubic feet",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": 0,
                                        "size": "5px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": 105,
                                        "size": "10px",
                                        "color": "rgb(96 2 2)",
                                    },
                                ],
                            },
                        },
                        "preferredRoute": {
                            "name": "Preferred Route",
                            "type": "toggle",
                            "help": "Whether the route is preferred",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": robot_path_locations_dict,
                        "valueLists": {
                            "capacity": [100],
                            "preferredRoute": [True],
                        },
                    },
                },
                "region": {
                    "type": "geo",
                    "name": "Warehouse Region",
                    "props": {
                        "isAvailable": {
                            "name": "Is Available",
                            "type": "toggle",
                            "help": "Whether this area is available",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": region_locations_dict,
                        "valueLists": {
                            "isAvailable": [True],
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
                        "square": {
                            "type": "map",
                            "mapId": "squareMap",
                        },
                        "landscape": {
                            "type": "map",
                            "mapId": "landscapeMap",
                        },
                        "portrait": {
                            "type": "map",
                            "mapId": "portraitMap",
                        },
                        "warehouse": {
                            "type": "map",
                            "mapId": "warehouseMap",
                        },
                    },
                    "pageLayout": ["square", "landscape", "portrait", "warehouse"],
                },
            },
        },
    }
