def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/4.10.1",
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
                },
            },
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
