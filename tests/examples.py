from cave_utils import Socket, Validator
import os, importlib


def get_examples():
    examples_location = "/app/cave_api/examples"
    return sorted(
        [
            i.replace(".py", "")
            for i in os.listdir(examples_location)
            if i.endswith(".py") and not i.startswith("__")
        ]
    )


def test_example(example_name):
    example_execute_command = importlib.import_module(
        f"cave_api.examples.{example_name}"
    ).execute_command
    session_data = example_execute_command(
        session_data={}, socket=Socket(silent=True), command="init"
    )

    validator = Validator(session_data, ignore_keys=["meta"])
    validator.log.print_logs()
    assert (
        len(validator.log.log) == 0
    ), f"Example `{example_name}.py` failed validation. See above logs for details."


if __name__ == "__main__":
    for example_name in get_examples():
        test_example(example_name)
