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
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": ["refreshButton", "session"],
            },
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
                # Add an appBar button to launch the sessions pane
                "session": {
                    "icon": "md/MdApi",
                    "type": "session",
                    "bar": "upperLeft",
                },
            },
        },
    }
