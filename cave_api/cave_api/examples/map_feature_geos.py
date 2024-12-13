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
                        "demandZones": {
                            "name": "Demand Zones",
                            "data": {
                                "custom": {
                                    "value": True,
                                    "icon": "pi/PiMountains",
                                    "colorBy": "booleanPropExample",
                                    "colorByOptions": ["numericPropExampleC", "booleanPropExample"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "custom": {
                    "type": "geo",
                    "name": "Custom",
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "min": 0,
                            "max": 100,
                            "unit": "units",
                            "help": "Help with the example numeric prop for this Custom",
                            "colorGradient": {
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "help": "Help for boolean prop",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "path": [
                                [
                                    [-75.447, 40.345],
                                    [-77.447, 42.345],
                                    [-77.447, 44.345],
                                    [-75.447, 40.345],
                                ]
                            ],
                        },
                        "valueLists": {
                            "numericPropExampleC": [100],
                            "booleanPropExample": [True],
                        },
                    },
                }
            },
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
