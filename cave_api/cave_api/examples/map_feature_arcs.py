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
            # Specify available map projections that can be selected in the dashboards by the user
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "globe",
                    # Specify the default viewport for the map
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
                        "transportation": {
                            "name": "Transportation",
                            "data": {
                                "unusualRoutes": {
                                    "value": True,
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": ["capacity", "preferredRoute"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "unusualRoutes": {
                    "type": "arc",
                    "name": "Unusual Routes",
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
                                    {"value": 0, "size": "5px", "color": "rgb(233 0 0)"},
                                    {"value": 105, "size": "10px", "color": "rgb(96 2 2)"},
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
                        "location": {
                            "path": [
                                # Boston to Albany to New York City path [longitude, latitude]
                                [
                                    [-71.0589, 42.3601],
                                    [-73.7562, 42.6526],
                                    [-74.0059, 40.7128],
                                ],
                                # Knoxville to Talahassee to Orlando path [longitude, latitude]
                                [
                                    [-83.9207, 35.9606],
                                    [-84.2533, 30.4383],
                                    [-81.3792, 28.5383],
                                ],
                            ]
                        },
                        "valueLists": {
                            "capacity": [75, 105],
                            "preferredRoute": [True, False],
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
                            "showToolbar": False,
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
            },
        },
    }
