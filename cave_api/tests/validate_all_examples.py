from cave_utils import Socket, Validator
import os, importlib.resources
from pprint import pprint as print


def get_examples():
    examples_location = "/app/cave_api/cave_api/examples"
    return sorted(
        [
            i.replace(".py", "")
            for i in os.listdir(examples_location)
            if i.endswith(".py") and not i.startswith("__")
        ]
    )


for i in get_examples():
    example_execute_command = importlib.import_module(f"cave_api.examples.{i}").execute_command
    session_data = example_execute_command(
        session_data={}, socket=Socket(silent=True), command="init"
    )

    x = Validator(session_data, ignore_keys=["meta"])
    if len(x.log.log) > 0:
        print(f"Example `{i}.py` failed validation.")
        print(x.log.log)
        break
