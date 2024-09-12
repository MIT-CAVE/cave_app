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
                # EG: https://react-icons.mitcave.com/5.0.1/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/5.0.1"
            },
            "appBar": {
                # Specify the order of items as they will appear in the app bar
                "order": {
                    "data": ["refreshButton", "myCommandButton"],
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
                    # `myCommandButton` is a custom button that is added to the app bar
                    # Buttons are be used to trigger custom back end logic
                    "myCommandButton": {
                        "icon": "md/MdLightbulbOutline",
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
        # Add your own custom logic here to modify the session data
        # EG - Toggle the icon between lightbulb and lightbulb outline
        current_icon = session_data["appBar"]["data"]["myCommandButton"]["icon"]
        # Update the icon in the session data
        session_data["appBar"]["data"]["myCommandButton"]["icon"] = (
            "md/MdLightbulb" if current_icon == "md/MdLightbulbOutline" else "md/MdLightbulbOutline"
        )
        # If you do not want to wipe the existing session data, you can set the `wipeExisting` flag to False
        # and only pass the top level keys that you want to update
        session_data = {'appBar':session_data['appBar'], 'extraKwargs':{'wipeExisting':False}}
        # Send a message to app users
        socket.notify("Notification: `myCommand` has been triggered!")
        # Log a message in the console
        print("Console Log: `myCommand` has been triggered!")
        # Return the updated session data
        return session_data
    # If no command is matched and handled above, raise an exception
    raise Exception(f"Command {command} not implemented")
