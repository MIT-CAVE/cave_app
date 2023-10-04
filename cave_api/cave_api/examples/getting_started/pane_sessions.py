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
                # Add a pane button to launch the sessions pane
                "session": {
                    "icon": "md/MdApi",
                    "type": "pane",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "data": {
                # Create a pane that allows the user to interact with sessions
                # Sessions represent the state of the app
                # A user (specifically a team) can have multiple sessions
                # Each session is a unique instance of the app
                # Note: This key must match the key used in the app bar above
                "session": {
                    "name": "Sessions Pane",
                    # By using the `session` variant, the pane will be rendered as a session pane
                    "variant": "session",
                },
            },
        },
    }
