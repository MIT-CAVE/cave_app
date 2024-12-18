def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": [
                    "examplePane",
                ],
            },
            "data": {
                # Add a pane to the app bar
                # This will add a button to the app bar that opens a pane
                # Panes are used to display additional options / data to the user
                # See the panes top level key below for more details
                "examplePane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "paneState": {
                "left": {"type": "pane", "open": "examplePane", "pin": False}
            },
            "data": {
                # Create a pane with an example header and simple numeric input
                # Note: This key must match the key used in the app bar above
                "examplePane": {
                    "name": "Example Options Pane",
                    # Create a set of example props to be rendered in the pane
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
                    # Layout is used to define the layout of props in a modal or pane
                    "layout": {
                        "type": "grid",
                        "numColumns": 2,
                        "numRows": 2,
                        "data": {
                            "col1Row1": {
                                "type": "item",
                                "column": 1,
                                "row": 1,
                                "itemId": "exampleHeader",
                            },
                            "col1Row2": {
                                "type": "item",
                                "column": 2,
                                "row": 2,
                                "itemId": "numericInputExample",
                            },
                        },
                    },
                    "values": {
                        "numericInputExample": 100,
                    },
                },
            },
        },
    }
