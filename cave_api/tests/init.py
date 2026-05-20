from cave_api.api import execute_command
from cave_utils import Socket, Validator


def test_init():
    init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

    validator = Validator(init_session_data, ignore_keys=["meta"])
    validator.log.print_logs()
    assert len(validator.log.log) == 0


if __name__ == "__main__":
    test_init()
