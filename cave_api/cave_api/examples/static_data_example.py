# This file is used to demonstrate how to access static files in the package
from pamda import pamda
from importlib import resources


# See `your_project/cave_api/cave_api/data` to see the data folder for this example
data_folder = resources.files("cave_api.data")
static_data_path = data_folder.joinpath("static_data_example.json").__str__()

def execute_command(session_data, socket, command="init", **kwargs):
    # `init` is the default command that is run when a session is created
    # It should return an initial state for the app
    if command == "init" or command == "reset":
        return pamda.read_json(static_data_path)
    # `info` is a custom command that is run when a user clicks on the info button
    # Command names are are arbitrary. They are defined at various places in the api.
    # For this example, `info` defined in the api in appBar.data.myCommandButton.apiCommand
    elif command == "info":
        # Send a message to app users
        socket.notify("This example loaded static data from a file!")
        # Return the updated session data
        return session_data
    # If no command is matched and handled above, raise an exception
    raise Exception(f"Command {command} not implemented")
