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
                # Add a pane button to launch the app settings pane
                "appSettings": {
                    "icon": "md/MdOutlineSettings",
                    "type": "pane",
                    "bar": "upperLeft",
                    "order": 1,
                },
            },
        },
        "panes": {
            "data": {
                # Create a pane that allows the user to interact with app settings
                # App settings are used to configure various aspects of the app
                # Note: This key must match the key used in the app bar above
                "appSettings": {
                    "name": "App Settings Pane",
                    # By using the `appSettings` variant, the pane will be rendered as an app settings pane
                    "variant": "appSettings",
                },
            },
        },
    }