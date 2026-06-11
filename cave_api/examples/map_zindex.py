def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": [
                    "mapGeosOnTopPage",
                    "mapArcsOnTopPage",
                ],
            },
            "data": {
                # Add appBar buttons to launch map-focused dashboards
                "mapGeosOnTopPage": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "upperLeft",
                    "name": "Geos On Top Map",
                },
                "mapArcsOnTopPage": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "upperLeft",
                    "name": "Arcs On Top Map",
                },
            },
        },
        "maps": {
            # Specify available map projections that can be selected in the dashboards by the user
            "data": {
                "mapGeosOnTop": {
                    "name": "Geos On Top Map",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "legendGroups": {
                        "objects": {
                            "name": "Objects",
                            "data": {
                                "arcs": {
                                    "value": True,
                                    "colorBy": "capacity",
                                    "colorByOptions": ["capacity"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    # Layered below geos
                                    "zIndex": 1,
                                },
                                "geos": {
                                    "value": True,
                                    "colorBy": "sentiment",
                                    "colorByOptions": ["sentiment"],
                                    # Layered above arcs
                                    "zIndex": 2,
                                },
                                "nodes": {
                                    "value": True,
                                    "colorBy": "capacity",
                                    "colorByOptions": ["capacity"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "icon": "fa6/FaWarehouse",
                                    # Note: nodes can only be ordered relative to each other at this time due to mapbox limitations.
                                    "zIndex": 3,
                                },
                            },
                        },
                    },
                },
                "mapArcsOnTop": {
                    "name": "Arcs On Top Map",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "legendGroups": {
                        "objects": {
                            "name": "Objects",
                            "data": {
                                "arcs": {
                                    "value": True,
                                    "colorBy": "capacity",
                                    "colorByOptions": ["capacity"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    # Layered above geos
                                    "zIndex": 2,
                                },
                                "geos": {
                                    "value": True,
                                    "colorBy": "sentiment",
                                    "colorByOptions": ["sentiment"],
                                    # Layered below arcs
                                    "zIndex": 1,
                                },
                                "nodes": {
                                    "value": True,
                                    "colorBy": "capacity",
                                    "colorByOptions": ["capacity"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "icon": "fa6/FaWarehouse",
                                    # Note: nodes can only be ordered relative to each other at this time due to mapbox limitations.
                                    "zIndex": 3,
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "arcs": {
                    "type": "arc",
                    "name": "Arcs",
                    "props": {
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "unit": "Cubic Feet",
                            "help": "The route capacity in shipments possible per week.",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": "min",
                                        "size": "5px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": "max",
                                        "size": "10px",
                                        "color": "rgb(96 2 2)",
                                    },
                                ],
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "path": [
                                [
                                    [-78.0, 42.0],
                                    [-72.0, 42.0],
                                ],
                                [
                                    [-78.0, 39.0],
                                    [-72.0, 39.0],
                                ],
                            ]
                        },
                        "valueLists": {
                            "capacity": [50, 100],
                        },
                    },
                },
                "geos": {
                    "type": "geo",
                    "name": "Geos",
                    "props": {
                        "sentiment": {
                            "name": "Sentiment",
                            "type": "num",
                            "unit": "units",
                            "help": "A value between 0 and 100 representing sentiment in this area",
                            "gradient": {
                                "data": [
                                    {"value": "min", "color": "rgb(0 0 255)"},
                                    {"value": "max", "color": "rgb(0 255 0)"},
                                ],
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "path": [
                                [
                                    [-76.0, 43.0],
                                    [-74.0, 43.0],
                                    [-74.0, 38.0],
                                    [-76.0, 38.0],
                                    [-76.0, 43.0],
                                ]
                            ],
                        },
                        "valueLists": {
                            "sentiment": [80],
                        },
                    },
                },
                "nodes": {
                    "type": "node",
                    "name": "Nodes",
                    "props": {
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "unit": "Cubic Feet",
                            "help": "Capacity in cubic feet",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": "min",
                                        "size": "30px",
                                        "color": "rgb(255 165 0)",
                                    },
                                    {
                                        "value": "max",
                                        "size": "45px",
                                        "color": "rgb(255 69 0)",
                                    },
                                ],
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[41.0]],
                            "longitude": [[-75.0]],
                        },
                        "valueLists": {
                            "capacity": [90],
                        },
                    },
                },
            },
        },
        # Add map pages to the app using the maps specified above
        "pages": {
            "currentPage": "mapGeosOnTopPage",
            "data": {
                "mapGeosOnTopPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "mapGeosOnTop",
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
                "mapArcsOnTopPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "mapArcsOnTop",
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
            },
        },
    }
