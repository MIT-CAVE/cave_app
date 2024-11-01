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
                        "transportation": {
                            "name": "Transportation",
                            "data": {
                                "unusualRoutes": {
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
                "unusualRoutes": {
                    "type": "arc",
                    "name": "Unusual Routes",
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
                            "path": [
                                # Boston to Albany to New York City path [longitude, latitude]
                                [[-71.0589, 42.3601], [-73.7562, 42.6526], [-74.0059, 40.7128]],
                                # Knoxville to Talahassee to Orlando path [longitude, latitude]
                                [[-83.9207, 35.9606], [-84.2533, 30.4383], [-81.3792, 28.5383]],
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
