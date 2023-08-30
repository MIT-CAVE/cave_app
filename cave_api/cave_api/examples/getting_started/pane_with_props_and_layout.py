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
                # Add a pane to the app bar
                # This will add a button to the app bar that opens a pane
                # Panes are used to display additional options / data to the user
                # See the panes top level key below for more details
                "examplePane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "bar": "upperLeft",
                    "order": 1,
                },
            },
        },
        "panes": {
            "data": {
                # Create a pane with an example header and simple numeric input
                # Note: This key must match the key used in the app bar above
                "examplePane": {
                    "name": "Example Options Pane",
                    # By using the `options` variant, the pane will be rendered as an options pane
                    # This allows for props to be rendered in the pane
                    "variant": "options",
                    # Create a set of example props to be rendered in the pane
                    "props": {
                        "topLeft": {
                            "name": "Top Left",
                            "type": "head",
                            # Convert the header variant from the default of col to row
                            # This creates a box rather than an underlined header
                            "variant": "row",
                        },
                        "bottomRight": {
                            "name": "Bottom Right",
                            "type": "head",
                            # Convert the header variant from the default of col to row
                            # This creates a box rather than an underlined header
                            "variant": "row",
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
                                "itemId": "topLeft",
                            },
                            "col1Row2": {
                                "type": "item",
                                "column": 2,
                                "row": 2,
                                "itemId": "bottomRight",
                            },
                        },
                    },
                },
            },
        },
    }