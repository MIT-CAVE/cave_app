from cave_api import execute_command
from cave_utils import Socket, Validator

from pprint import pp


init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

x = Validator(init_session_data)

x.print_errors()
x.print_warnings()

x.write_warnings('./warnings.txt')
x.write_errors('./errors.txt')
