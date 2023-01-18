from cave_api import execute_command

init_session_data = execute_command(session_data={}, command="init")

from pprint import pprint
pprint(init_session_data)
