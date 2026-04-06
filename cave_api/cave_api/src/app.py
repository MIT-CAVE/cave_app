# This is the starting template for your own Cave API app.
# To activate it, open cave_api/cave_api/api.py and uncomment Option 2.
#
# The execute_command function is the sole entry point for the Cave API.
# It receives the current app state (session_data), the socket for
# sending messages to the user, and a command string. It must return
# the updated session_data dict.
#
# See cave_api/README.md for full documentation and examples.

def execute_command(session_data, socket, command="init", **kwargs):
    return {
            "settings": {
                # Icon Url is used to load icons from a custom icon library
                # See the available versions provided by the cave team here:
                # https://react-icons.mitcave.com/versions.txt
                # Once you select a version, you can see the available icons in the version
                # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/5.4.0"
            },
    }
