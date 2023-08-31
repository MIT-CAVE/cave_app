def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            "data": {
                # Icon Url is used to load icons from a custom icon library
                # See the available versions provided by the cave team here: 
                # https://react-icons.mitcave.com/versions.txt
                # Once you select a version, you can see the available icons in the version
                # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/4.10.1"
            },
        },
        "appBar": {
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                    "order": 0,
                },
                # Add a pane button to launch a map focused dashboard
                "mapDashboard": {
                    "icon": "md/MdMap",
                    "type": "stats",
                    "bar": "upperLeft",
                    "order": 1,
                },
            },
        },
        "maps": {
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "height": 1287,
                        "altitude": 1.5,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                },
            },
        },
        "dashboards": {
            "data": {
                "mapDashboard": {
                    "dashboardLayout": [
                        {
                            "type": "maps",
                            "mapId": "exampleMap"
                        },
                    ],
                },
            },
        },
    }