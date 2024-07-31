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
            "order": {"data": ["refreshButton", "mapPage"]},
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
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
                        "facilities": {
                            "name": "Facilities",
                            "data": {
                                "warehouse": {
                                    "value": True,
                                    "sizeBy": "capacity",
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
                                    "sizeByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startSize": "30px",
                                            "endSize": "45px",
                                        },
                                    },
                                    "icon": "fa6/FaWarehouse",
                                },
                            },
                        },
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
                                    "icon": "bs/BsHexagon",
                                },
                            },
                        },
                        "transportation": {
                            "name": "Transportation",
                            "data": {
                                "truckRoutes": {
                                    "value": True,
                                    "sizeBy": "capacity",
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
                                    "sizeByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 80,
                                            "startSize": "5px",
                                            "endSize": "10px",
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
                            "enabled": True,
                            "help": "The warehouse capacity in cubic feet",
                            "unit": "Cubic Feet",
                            "legendNotation": "precision",
                            "legendPrecision": 0,
                        },
                        "includesAutomation": {
                            "name": "Includes Automation",
                            "type": "toggle",
                            "enabled": True,
                            "help": "Whether the warehouse includes automation",
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[43.78, 39.82]],
                            "longitude": [[-79.63, -86.18]],
                            "height": [[0.4, 0.6]],
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
                            "enabled": True,
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
                            "enabled": True,
                            "help": "The warehouse capacity in cubic feet",
                            "unit": "Cubic Feet",
                            "legendNotation": "precision",
                            "legendPrecision": 0,
                        },
                        "preferredRoute": {
                            "name": "Preferred Route",
                            "type": "toggle",
                            "enabled": True,
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
            }
        },
        # Add a map page to the app using the example map specified above
        "pages": {
            "currentPage": "mapPage",
            "data": {
                "mapPage": {
                    "pageLayout": [
                        {
                            "type": "map",
                            "mapId": "exampleMap",
                            "showToolbar": False,
                            "maximized": True,
                        },
                    ],
                },
            },
        },
    }
