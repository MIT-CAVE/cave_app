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
                "data": ["refreshButton", "exampleModal"],
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
            "paneState":{"center":{"type":"pane", "open":"exampleModal", "pinned":True}},
            "data": {
                # Create a modal with an example header and simple numeric input
                # Note: This key must match the key used in the app bar above
                "exampleModal": {
                    "name": "Example Modal",
                    "variant": "options",
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
