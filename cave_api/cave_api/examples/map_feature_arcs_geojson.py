def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/4.10.1"
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
                                "specialRoutes": {
                                    "value": True,
                                    "sizeBy": "capacity",
                                    "colorBy": "preferredRoute",
                                    "colorByOptions": {
                                        "capacity": {
                                            "min": 0,
                                            "max": 105,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "preferredRoute": {
                                            "false": "rgba(255,0,0, 255)",
                                            "true": "rgba(0,255,0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "capacity": {"min": 0, "max": 80, "startSize": "5px", "endSize": "10px"},
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
                "specialRoutes": {
                    "type": "arc",
                    "name": "Special Routes",
                    "geoJson": {
                        # geoJsonLayer must be a URL pointing to a raw geojson file
                        # Local file support is not supported
                        # To upload your own geojson file, use a service like GitHub and upload your file there
                        # Then copy the raw URL and paste it in the geoJsonLayer field to use it
                        # See data in cave_api/cave_api/example_data/example.geojson
                        "geoJsonLayer": "https://raw.githubusercontent.com/MIT-CAVE/cave_app/ced363/cave_api/cave_api/example_data/example.geojson",
                        # geoJsonProp is the property in the geoJson file that contains the id you specify in the data.location.geoJsonValue field
                        "geoJsonProp": "arc_id",
                    },
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
                            # geoJsonValue must be a list of ids that match the geoJsonProp in the geoJson file
                            # The order of the ids must match the order of the values in the data.values fields
                            "geoJsonValue": ["toronto-pittsburgh-indianapolis", "souix-falls-little-rock-memphis"],
                        },
                        "valueLists": {
                            "capacity": [65, 85],
                            "preferredRoute": [True, False],
                        },
                    }
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
                            "maximized": True},
                    ],
                },
            },
        },
    }
