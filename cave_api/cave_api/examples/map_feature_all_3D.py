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
                                "state": {
                                    "value": True,
                                    "colorBy": "targetGrowthArea",
                                    "colorByOptions": ["demand", "targetGrowthArea"],
                                    "heightBy": "demand",
                                    "heightByOptions": ["demand"],
                                    "icon": "pi/PiMountains",
                                },
                            },
                        },
                        "facilities": {
                            "name": "Facilities",
                            "data": {
                                "warehouse": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "colorBy": "includesAutomation",
                                    "colorByOptions": [
                                        "capacity",
                                        "includesAutomation",
                                    ],
                                    "icon": "fa6/FaWarehouse",
                                },
                            },
                        },
                        "transportation": {
                            "name": "Transportation",
                            "data": {
                                "truckRoutes": {
                                    "value": True,
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": ["capacity", "preferredRoute"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "heightBy": "capacity",
                                    "heightByOptions": ["capacity"],
                                },
                                "specialRoutes": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": ["capacity", "preferredRoute"],
                                    "heightBy": "capacity",
                                    "heightByOptions": ["capacity"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "warehouse": {
                    "type": "node",
                    "name": "Warehouse",
                    "props": {
                        "scenario": {
                            "name": "Scenario",
                            "type": "text",
                            "enabled": False,
                            "display": False,
                            "help": "The scenario name",
                        },
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "min": 0,
                            "max": 100,
                            "unit": "Cubic Feet",
                            "help": "The warehouse capacity in cubic feet",
                            "sizeGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "30px"},
                                    {"value": "max", "size": "45px"},
                                ],
                            },
                            "colorGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                        },
                        "includesAutomation": {
                            "name": "Includes Automation",
                            "type": "toggle",
                            "help": "Whether the warehouse includes automation",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[43.78, 39.82]],
                            "longitude": [[-79.63, -86.18]],
                            "height": [[0.8, 0.6]],
                        },
                        "valueLists": {
                            "capacity": [100, 80],
                            "includesAutomation": [True, False],
                            "scenario": ["Scenario 1", "Scenario 2"],
                        },
                    },
                },
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
                            "min": 0,
                            "max": 100,
                            "unit": "units",
                            "help": "Demand for this state",
                            "colorGradient": {
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                            "heightGradient": {
                                "data": [
                                    {"value": "min", "height": "10px"},
                                    {"value": "max", "height": "40px"},
                                ]
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
                "truckRoutes": {
                    "type": "arc",
                    "name": "Truck Routes",
                    "props": {
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "min": 0,
                            "max": 105,
                            "unit": "Cubic Feet",
                            "help": "The warehouse capacity in cubic feet",
                            "colorGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                            "sizeGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "5px"},
                                    {"value": "max", "size": "10px"},
                                ],
                            },
                            "heightGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "height": "10px"},
                                    {"value": "max", "height": "40px"},
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
                            "startLatitude": [43.78, 39.82],
                            "startLongitude": [-79.63, -86.18],
                            "startHeight": [0.4, 0.6],
                            "endLatitude": [39.82, 39.95],
                            "endLongitude": [-86.18, -75.16],
                            "endHeight": [0.6, 0.1],
                        },
                        "valueLists": {
                            "capacity": [75, 105],
                            "preferredRoute": [True, False],
                        },
                    },
                },
                "specialRoutes": {
                    "type": "arc",
                    "name": "Special Routes",
                    "geoJson": {
                        # geoJsonLayer must be a URL pointing to a raw geojson file
                        # Local file support is not supported
                        # To upload your own geojson file, use a service like GitHub and upload your file there
                        # Then copy the raw URL and paste it in the geoJsonLayer field to use it
                        # See data in https://github.com/MIT-CAVE/cave_app_extras/tree/main/example_data
                        "geoJsonLayer": "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/main/example_data/example.geojson",
                        # geoJsonProp is the property in the geoJson file that contains the id you specify in the data.location.geoJsonValue field
                        "geoJsonProp": "arc_id",
                    },
                    "props": {
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "min": 0,
                            "max": 105,
                            "unit": "Cubic Feet",
                            "help": "The warehouse capacity in cubic feet",
                            "colorGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "color": "rgb(233 0 0)"},
                                    {"value": "max", "color": "rgb(96 2 2)"},
                                ],
                            },
                            "sizeGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "5px"},
                                    {"value": "max", "size": "10px"},
                                ],
                            },
                            "heightGradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "height": "10px"},
                                    {"value": "max", "height": "40px"},
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
                            # geoJsonValue must be a list of ids that match the geoJsonProp in the geoJson file
                            # The order of the ids must match the order of the values in the data.values fields
                            "geoJsonValue": [
                                "toronto-pittsburgh-indianapolis",
                                "souix-falls-little-rock-memphis",
                            ],
                        },
                        "valueLists": {
                            "capacity": [65, 85],
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
