from pamda import pamda
import os, importlib.resources

# This file is not intended to serve as an example, but rather is used as a way to serve up examples
# You should not consider this as code to emulate, but rather as a way to serve up examples


def get_examples():
    # Return all the examples in the cave_api/examples folder
    examples_location = importlib.resources.files("cave_api") / "cave_api" / "examples"
    return sorted(
        [
            i.replace(".py", "")
            for i in os.listdir(examples_location)
            if i.endswith(".py") and i != "__init__.py" and i != "example_selector.py"
        ]
    )


def execute_command(session_data, socket, command="init", **kwargs):
    # Get the currently selected example name if it exists
    selected_example = pamda.pathOr(
        [None], ["panes", "data", "exampleSelector", "values", "example"], session_data
    )[0]
    # Get a list of all available examples
    examples = get_examples()
    # Ensure that the selected example is valid
    if selected_example not in examples:
        selected_example = examples[0]
    # Import the selected example's execute_command function
    example_execute_command = importlib.import_module(
        f"cave_api.examples.{selected_example}"
    ).execute_command

    # A data structure to hold the persistent pane for selecting an example to preview
    exampleSelectorPane = {
        "name": "Example Code Selector",
        "props": {
            "example": {
                "name": "Example Code To Preview",
                "type": "selector",
                "variant": "radio",
                "help": "Select an example to preview",
                "options": {k: {"name": k + ".py"} for k in examples},
                "apiCommand": "init",
            },
            "note": {
                "name": "Note",
                "type": "text",
                "variant": "textarea",
                "rows": 13,
                "help": "This is a note to help you understand how to use the example selector pane.",
            },
        },
        "values": {
            "example": [selected_example],
            "note": "Select one of the example files above to preview an app using that code.\n\nTo view the code for each example, open the corresponding file in:\n\ncave_api/cave_api/examples\n\nYou can add or modify examples. Your changes will be reflected the next time you select that example from the above list.",
        },
    }

    # A data structure to hold the persistent app bar button for selecting an example to preview
    exampleSelectorAppBarButton = {
        "icon": "fa/FaSlidersH",
        "type": "pane",
        "bar": "upperLeft",
    }

    # Execute the selected example's execute_command function
    session_data = example_execute_command(session_data, socket, command, **kwargs)

    # Add the example selector pane and app bar button to the session data and set it as first in the app bar order
    appBarOrder = ["exampleSelector"] + pamda.pathOr([], ["appBar", "order", "data"], session_data)
    pamda.assocPath(["appBar", "order", "data"], appBarOrder, session_data)
    pamda.assocPath(["panes", "data", "exampleSelector"], exampleSelectorPane, session_data)
    pamda.assocPath(
        ["appBar", "data", "exampleSelector"], exampleSelectorAppBarButton, session_data
    )
    # When reinitializing a session, wipe the existing session data
    if command == "init":
        pamda.assocPath(["extraKwargs", "wipeExisting"], True, session_data)

    # Return the modified session data from the selected example's execute_command function
    return session_data
