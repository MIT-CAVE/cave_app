from cave_api import execute_command
from cave_utils import Socket, Validator


init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

x = Validator(init_session_data, version="0.0.0")
x.check_top_level_keys()

print("test_init.py passed!")
