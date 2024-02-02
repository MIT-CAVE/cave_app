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
            # Specify to not sync the center pane state with the server
            # This will prevent other users in the same session from seeing launced modals from other clients in the same session
            # NOTE: By default, everything in the API is synced with the server
            #    - Only items that are synced with the server are able to be sent as `session_data` to this `execute_command` function
            #    - This means that you should only de-sync data if it is not needed / relevant in the `execute_command` function
            "sync": {
                # Specify an arbitrary name for each sync group (for use with pathing and validation purposes)
                "launchedModal": {
                    # Specify the name of the data item to sync (only relevant if `showToggle` is `True`)
                    "name": "Launched Modal",
                    # Specify if a special sync toggle should be shown in the settings pane.
                    "showToggle": True,
                    # Specify the default value of weather or not to sync the data item
                    # NOTE: This value defaults to True if not specified
                    "value": False,
                    # Specify your sync data paths here
                    "data": {
                        # Specify the path to the data item to sync
                        # NOTE: The key is arbitrary and can be anything you want (for use with pathing and validation purposes)
                        # NOTE: The value is a list of keys that specify the path to the data item to sync/de-sync (depending on `value` above)
                        "lm1": ["panes", "paneState", "center"]
                    },
                },
            },
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": ["refreshButton", "settingsPane" "exampleModal"],
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
                # Add an appBar button to launch the app settings pane
                "appSettings": {
                    "icon": "md/MdOutlineSettings",
                    "type": "settings",
                    "bar": "upperLeft",
                },
                # Add a modal to the app bar
                # This will add a button to the app bar that opens a modal
                # Modals are used to display additional options / data to the user
                # See the modals top level key below for more details
                "exampleModal": {
                    "icon": "fa/FaSlidersH",
                    "type": "pane",
                    "variant": "modal",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "paneState": {"center": {"type": "pane", "open": "exampleModal", "pin": True}},
            "data": {
                # Create a modal with an example header and simple numeric input
                # Note: This key must match the key used in the app bar above
                "exampleModal": {
                    "name": "Example Modal",
                    "props": {
                        "exampleHeader": {
                            "name": "Example Header",
                            "type": "head",
                            "help": "Some help for the Example Header",
                        },
                        "numericInputExample": {
                            "name": "Numeric Input Example",
                            "type": "num",
                            "help": "Help for the numeric input example",
                            "unit": "widgets",
                        },
                    },
                    "values": {
                        "numericInputExample": 100,
                    },
                },
            },
        },
    }
