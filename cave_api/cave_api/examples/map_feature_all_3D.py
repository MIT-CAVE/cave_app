def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.0.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.0.1"
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
                                    "colorByOptions": {
                                        "demand": {
                                            "min": 0,
                                            "max": 100,
                                            "startGradientColor": "rgba(233, 0, 0, 1)",
                                            "endGradientColor": "rgba(96, 2, 2, 1)",
                                        },
                                        "targetGrowthArea": {
                                            "false": "rgba(255, 0, 0, 1)",
                                            "true": "rgba(0, 255, 0, 1)",
                                        },
                                    },
                                    "heightBy": "demand",
                                    "heightByOptions": {
                                        "demand": {
                                            "min": 0,
                                            "max": 80,
                                            "startHeight": "10px",
                                            "endHeight": "40px",
                                        },
                                    },
                                    "icon": "bs/BsHexagon",
                                },
                            },
                        },
                        "facilities": {
                            "name": "Facilities",
                            "data": {
                                "warehouse": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "sizeByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startSize": "30px",
                                            "endSize": "45px",
                                        },
                                    },
                                    "colorBy": "includesAutomation",
                                    "colorByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 100,
                                            "startGradientColor": "rgba(233, 0, 0, 1)",
                                            "endGradientColor": "rgba(96, 2, 2, 1)",
                                        },
                                        "includesAutomation": {
                                            "false": "rgba(255, 0, 0, 1)",
                                            "true": "rgba(0, 255, 0, 1)",
                                        },
                                    },
                                    "icon": "fa6/FaWarehouse",
                                },
                            },
                        },
                        "transportation": {
                            "name": "Transportation",
                            "data": {
                                "truckRoutes": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "sizeByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startSize": "5px",
                                            "endSize": "10px",
                                        },
                                    },
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 105,
                                            "startGradientColor": "rgba(233, 0, 0, 1)",
                                            "endGradientColor": "rgba(96, 2, 2, 1)",
                                        },
                                        "preferredRoute": {
                                            "false": "rgba(255, 0, 0, 1)",
                                            "true": "rgba(0, 255, 0, 1)",
                                        },
                                    },
                                    "heightBy": "capacity",
                                    "heightByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startHeight": "10px",
                                            "endHeight": "40px",
                                        },
                                    },
                                },
                                "specialRoutes": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "sizeByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startSize": "5px",
                                            "endSize": "10px",
                                        },
                                    },
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 105,
                                            "startGradientColor": "rgba(233, 0, 0, 1)",
                                            "endGradientColor": "rgba(96, 2, 2, 1)",
                                        },
                                        "preferredRoute": {
                                            "false": "rgba(255, 0, 0, 1)",
                                            "true": "rgba(0, 255, 0, 1)",
                                        },
                                    },
                                    "heightBy": "capacity",
                                    "heightByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startHeight": "10px",
                                            "endHeight": "40px",
                                        },
                                    },
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
                            "help": "The warehouse capacity in cubic feet",
                            "unit": "Cubic Feet",
                            "legendNotation": "precision",
                            "legendPrecision": 0,
                        },
                        "includesAutomation": {
                            "name": "Includes Automation",
                            "type": "toggle",
                            "help": "Whether the warehouse includes automation",
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
                            "help": "Demand for this state",
                            "unit": "units",
                        },
                        "targetGrowthArea": {
                            "name": "Target Growth Area",
                            "type": "toggle",
                            "help": "Whether this state is a target growth area for the company",
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
                            "help": "The warehouse capacity in cubic feet",
                            "unit": "Cubic Feet",
                            "legendNotation": "precision",
                            "legendPrecision": 0,
                        },
                        "preferredRoute": {
                            "name": "Preferred Route",
                            "type": "toggle",
                            "help": "Whether the route is preferred",
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
                            "help": "The warehouse capacity in cubic feet",
                            "unit": "Cubic Feet",
                            "legendNotation": "precision",
                            "legendPrecision": 0,
                        },
                        "preferredRoute": {
                            "name": "Preferred Route",
                            "type": "toggle",
                            "help": "Whether the route is preferred",
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
