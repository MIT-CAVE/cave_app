from cave_api.api import execute_command
from cave_utils import Socket, Validator
from pamda import pamda
import json
import os

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutation_logs")


def parse_field(value):
    if value is None or value == "" or value == "null":
        return None
    if isinstance(value, str):
        return json.loads(value)
    return value


def parse_log(log_path):
    if log_path.endswith(".json"):
        raw_events = pamda.read_json(log_path)
    elif log_path.endswith(".csv"):
        raw_events = pamda.read_csv(log_path)
    else:
        raise ValueError(f"Unsupported log file format for file: {log_path}")
    if not isinstance(raw_events, list):
        raise ValueError(
            f"Expected log file to contain a list of events, but got: {type(raw_events)}"
        )
    events = []
    session_ids = set()
    for i, raw_event in enumerate(raw_events):
        if not isinstance(raw_event, dict):
            raise ValueError(
                f"Expected each event to be a dictionary, but got: {type(raw_event)} at index {i}"
            )
        event = {}
        event["data_path"] = parse_field(raw_event.get("data_path")) or []
        event["data_value"] = parse_field(raw_event.get("data_value"))
        event["api_command_keys"] = parse_field(raw_event.get("api_command_keys"))
        event["api_command"] = raw_event.get("api_command")
        event["data_name"] = raw_event.get("data_name")
        event["timestamp"] = raw_event.get("timestamp")
        session_ids.add(raw_event.get("session_id"))
        events.append(event)
    assert (
        len(session_ids) == 1
    ), "Log contains events from multiple sessions, which is not supported."
    return sorted(events, key=lambda x: x["timestamp"])


def validate(session_data: dict, message: str = "", do_validate: bool = True):
    if do_validate:
        validator = Validator(session_data, ignore_keys=["meta"])
        if validator.log.log:
            validator.log.print_logs()
            raise Exception("Session data validation failed. " + message)


def replay_events(events, validate_each_step=False):
    socket = Socket(silent=True)
    session_data = execute_command(session_data={}, socket=socket, command="init")
    validate(
        session_data,
        message="Initial session data validation failed after init command.",
        do_validate=validate_each_step,
    )
    for event in events:
        if event.get("data_name"):
            session_data = pamda.assocPath(
                path=[event.get("data_name")] + event.get("data_path"),
                value=event.get("data_value"),
                data=session_data,
            )
        if event.get("api_command"):
            session_data = execute_command(
                session_data=session_data, socket=socket, command=event.get("api_command")
            )
        validate(
            session_data,
            message=f"Session data validation failed after processing event with API command: {event.get('api_command')}",
            do_validate=validate_each_step,
        )
    validate(
        session_data, message="Final session data validation failed after replay.", do_validate=True
    )
    return session_data


def test_all_logs():
    for log_file in os.listdir(LOGS_DIR):
        if not log_file.endswith(".json") and not log_file.endswith(".csv"):
            continue
        log_path = os.path.join(LOGS_DIR, log_file)
        print(f"Replaying events from log: {log_path}")
        events = parse_log(log_path)
        replay_events(events, validate_each_step=True)
        print(f"Successfully replayed events from log: {log_path}\n")


if __name__ == "__main__":
    test_all_logs()
