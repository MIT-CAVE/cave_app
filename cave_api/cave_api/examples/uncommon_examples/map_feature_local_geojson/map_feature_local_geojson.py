from cave_core import models


def execute_command(session_data, socket, command="init", **kwargs):
    # Before using this example, make sure to upload the geojson file to the server
    # See the file: cave_api/cave_api/examples/gen_pretty_route_geojson.py
    # Go to admin -> File Storage -> Add File
    # Upload the geojson file from data and set the name to "multi_route"

    # Get the URL of the uploaded geojson file
    # On cloud servers, the URL generated should be a full path to a file in the file server (aws, azure, etc.)
    # On local servers, the URL generated should be preceded by "http://localhost:8000"
    multi_route_path = (
        "http://localhost:8000"
        + models.FileStorage.objects.filter(name="multi_route").first().file_public.url
    )
    # If you choose to use a private file on a cloud server
    # - It is accessed the same way as the public file
    # - The returned url will be a temporary url that can be used to access the file
    # - The url will expire after a certain amount of time
    # - The url can be accessed by using `file_private.url` instead of `file_public.url`
    # - This can cause issues where users may need to reset/reinitialize the app to regain access to the file
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
                "specialRoutes": {
                    "type": "arc",
                    "name": "Special Routes",
                    "geoJson": {
                        # geoJsonLayer must be a URL pointing to a raw geojson file
                        # Local file support is not supported
                        # To upload your own geojson file, use a service like GitHub and upload your file there
                        # Then copy the raw URL and paste it in the geoJsonLayer field to use it
                        # See data in https://github.com/MIT-CAVE/cave_app_extras/tree/main/example_data
                        "geoJsonLayer": multi_route_path,
                        # geoJsonProp is the property in the geoJson file that contains the id you specify in the data.location.geoJsonValue field
                        "geoJsonProp": "id",
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
                                "Baltimore-London",
                                "Baltimore-Paris",
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
