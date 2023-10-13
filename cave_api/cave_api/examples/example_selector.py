from pamda import pamda
import os, importlib.resources

def get_examples():
    examples_location = importlib.resources.files("cave_api") / "cave_api" / "examples"
    return sorted([i.replace('.py','') for i in os.listdir(examples_location) if i.endswith('.py') and i != '__init__.py' and i != 'example_selector.py'])

def execute_command(session_data, socket, command="init", **kwargs):
    selected_pane = pamda.pathOr([None],['panes','data','exampleSelector','values','example'], session_data)[0]
    examples = get_examples()
    if selected_pane not in examples:
        selected_pane = examples[0]
    example_execute_command = importlib.import_module(f'cave_api.examples.{selected_pane}').execute_command
    
    exampleSelectorPane = {
        "name": "Example Code Selector",
        "variant": "options",
        "props": {
            "example": {
                "name": "Example Code To Preview",
                "type": "selector",
                "variant": "radio",
                "help": "Select an example to preview",
                "options": {k:{'name':k+'.py'} for k in examples},
                "apiCommand": "init",
            },
        },
        "values": {
            "example": [selected_pane],
        },
    }
    
    exampleSelectorAppBarButton = {
        "icon": "fa/FaSlidersH",
        "type": "pane",
        "bar": "upperLeft",
    }

    session_data = example_execute_command(session_data, socket, command, **kwargs)
    
    appBarOrder = ['exampleSelector'] + pamda.pathOr([], ['appBar','order','data'], session_data)

    pamda.assocPath(['appBar','order','data'], appBarOrder, session_data)
    pamda.assocPath(['panes','data','exampleSelector'], exampleSelectorPane, session_data)
    pamda.assocPath(['appBar','data','exampleSelector'], exampleSelectorAppBarButton, session_data)
    return session_data

