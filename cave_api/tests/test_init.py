from cave_api import execute_command
from cave_utils.socket import Socket
from cave_utils.validator import Validator


init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

x = Validator(init_session_data)

x.log.print_logs()
# x.print_warnings()
# x.write_warnings('./warnings.txt')
# x.write_errors('./errors.txt')
