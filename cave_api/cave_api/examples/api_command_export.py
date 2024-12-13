import json

def execute_command(session_data, socket, command="init", **kwargs):
    # `init` is the default command that is run when a session is created
    # It should return an initial state for the app
    if command == "init":
        session_data = {
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
                        "myCommandButton",
                    ],
                },
                "data": {
                    # `myCommandButton` is a custom button that is added to the app bar
                    # Buttons are be used to trigger custom back end logic
                    "myCommandButton": {
                        "icon": "md/MdFileDownload",
                        "apiCommand": "myCommand",
                        "type": "button",
                        "bar": "upperLeft",
                    },
                },
            },
        }
        return session_data
    # `myCommand` is a custom command that is run when a user clicks on a button
    # Command names are are arbitrary. They are defined at various places in the api.
    # For this example, `myCommand` defined in the api in appBar.data.myCommandButton.apiCommand
    elif command == "myCommand":
        # Send the current session data to app users
        socket.export(f'data:application/json,{json.dumps(session_data)}')
        # Log a message in the console
        print("Console Log: `myCommand` has been triggered!")
        return session_data
    # If no command is matched and handled above, raise an exception
    raise Exception(f"Command {command} not implemented")
