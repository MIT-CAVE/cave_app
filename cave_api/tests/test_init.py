from cave_api.examples.kitchen_sink import execute_command
from cave_utils import Socket, Validator


init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

x = Validator(init_session_data, ignore_keys=["meta"])

x.log.print_logs()
x.log.write_logs(path="./logs/validation/log.txt")
