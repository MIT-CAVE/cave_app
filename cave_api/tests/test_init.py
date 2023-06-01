from cave_api import execute_command
from cave_utils import Socket, Validator


init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

Validator(init_session_data, version="0.0.0")

print("test_init.py passed!")
