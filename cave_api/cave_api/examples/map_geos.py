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
                        "coreGeographicRegions": {
                            "name": "Core Geographic Regions",
                            "data": {
                                "state": {
                                    "value": True,
                                    "icon": "bs/BsHexagon",
                                    "colorBy": "targetGrowthArea",
                                    "colorByOptions": ["demand", "targetGrowthArea"],
                                },
                                "customGeoJson": {
                                    "value": True,
                                    "icon": "pi/PiMountains",
                                    "colorBy": "isTargetArea",
                                    "colorByOptions": ["customerSentiment", "isTargetArea"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "state": {
                    "type": "geo",
                    "name": "State",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                        "geoJsonProp": "code_hasc",
                    },
                    "props": {
                        "demand": {
                            "name": "Demand",
                            "type": "num",
                            "unit": "units",
                            "help": "Demand for this state",
                            "gradient": {
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": 100, "color": "rgb(96 2 2)"},
                                ],
                            },
                        },
                        "targetGrowthArea": {
                            "name": "Target Growth Area",
                            "type": "toggle",
                            "help": "Whether this state is a target growth area for the company",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "geoJsonValue": ["CA.ON", "US.MI", "US.PA"],
                        },
                        "valueLists": {
                            "demand": [50, 80, 75],
                            "targetGrowthArea": [False, False, True],
                        },
                    },
                },
                "customGeoJson": {
                    "type": "geo",
                    "name": "Custom",
                    "props": {
                        "customerSentiment": {
                            "name": "Customer Sentiment",
                            "type": "num",
                            "unit": "units",
                            "help": "A value between 0 and 100 representing customer sentiment in this area",
                            "gradient": {
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                        },
                        "isTargetArea": {
                            "name": "Is Target Area",
                            "type": "toggle",
                            "help": "Whether this area is a target area for the company",
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
                                    [-77.447, 41.176],
                                    [-78.447, 40.561],
                                    [-75.447, 40.345],
                                ]
                            ],
                        },
                        "valueLists": {
                            "customerSentiment": [100],
                            "isTargetArea": [True],
                        },
                    },
                },
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
