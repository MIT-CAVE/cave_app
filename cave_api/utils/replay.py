from pamda import pamda
import json

from cave_api.api import execute_command
from cave_utils import Socket, Validator

from typing import Callable, Literal
import type_enforced

@type_enforced.Enforcer
class Replay:
    """
    Replays a recorded mutation log against execute_command, rebuilding session
    state event-by-event.

    Useful for reproducing bugs, regression testing specific user sessions, or
    validating that a refactored API produces identical output for a known input
    sequence.

    Example:

    ```
    from cave_api.utils.replay import Replay
    replay = Replay("path/to/mutation_log.csv")
    replay.advance("all")
    ```
    """

    def __init__(self,
            mutation_log_file:str,
            sort_by_timestamp:bool=True,
            execute_command:Callable=execute_command,
            ignore_keys:list[str]=['meta'],
            print_on_invalid:bool=True,
            raise_on_invalid:bool=True
        ):
        """
        Requires:

        - `mutation_log_file`:
            - Type: str
            - What: Path to a `.json` or `.csv` mutation log
            - Note: Must contain events from a single session only

        Optional:

        - `sort_by_timestamp`:
            - Type: bool
            - What: Re-order events by `timestamp` before replay
            - Default: True
            - Note: Set to False only if you want your log to be processed in the exact input order (useful for custom sorting)
        - `execute_command`:
            - Type: Callable
            - What: The API entry point to replay against
            - Default: execute command imported from cave_api.api
            - Note: Override to test a refactored version side-by-side
        - `ignore_keys`:
            - Type: list[str]
            - What: Keys skipped by the validator
            - Default: ['meta']
        - `print_on_invalid`:
            - Type: bool
            - What: Whether to print validation errors to stdout when session data is invalid
            - Default: True
        - `raise_on_invalid`:
            - Type: bool
            - What: Whether to raise an exception on validation failure
            - Default: True
            - Note: Set to False to continue replay despite invalid state (useful for diagnostics)
        """
        self.__mutation_log_file__ = mutation_log_file
        self.__current_step__ = -1
        self.__socket__ = Socket(silent=True)

        self.__ignore_keys__=ignore_keys
        self.__print_on_invalid__=print_on_invalid
        self.__raise_on_invalid__=raise_on_invalid

        self.__get_events__(sort_by_timestamp=sort_by_timestamp)

        self.session_data = None
        self.execute_command = execute_command

    def __serialize_field__(self, value):
        if value is None or value == "" or value == "null":
            return None
        if isinstance(value, str):
            return json.loads(value)
        return value
    
    def __get_events__(self, sort_by_timestamp:bool=True):
        # Read in Raw Events
        if self.__mutation_log_file__.endswith(".json"):
            raw_events = pamda.read_json(self.__mutation_log_file__)
        elif self.__mutation_log_file__.endswith(".csv"):
            raw_events = pamda.read_csv(self.__mutation_log_file__)
        else:
            raise ValueError(f"Unsupported log file format for file: {self.__mutation_log_file__}")
        
        if not isinstance(raw_events, list):
            raise ValueError(
                f"Expected log file to contain a list of events, but got: {type(raw_events)}"
            )
        if len(raw_events) == 0:
            raise ValueError("Log file contains no events.")

        # Clean Events
        events = []
        session_ids = set()
        for i, raw_event in enumerate(raw_events):
            if not isinstance(raw_event, dict):
                raise ValueError(
                    f"Expected each event to be a dictionary, but got: {type(raw_event)} at index {i}"
                )
            event = {}
            event["data_path"] = self.__serialize_field__(raw_event.get("data_path")) or []
            event["data_value"] = self.__serialize_field__(raw_event.get("data_value"))
            event["api_command_keys"] = self.__serialize_field__(raw_event.get("api_command_keys"))
            event["api_command"] = raw_event.get("api_command")
            event["data_name"] = raw_event.get("data_name")
            event["timestamp"] = raw_event.get("timestamp")
            session_ids.add(raw_event.get("session_id"))
            events.append(event)
        assert (
            len(session_ids) == 1
        ), "Log contains events from multiple sessions, which is not supported."
        if sort_by_timestamp:
            raw_events = sorted(raw_events, key=lambda x: x["timestamp"])
            events = sorted(events, key=lambda x: x["timestamp"])
        
        # Store the events
        self.raw_events = raw_events
        self.events = events

    def __execute_step__(self):
        event = self.events[self.__current_step__]
        if event.get("data_name"):
            self.session_data = pamda.assocPath(
                path=[event.get("data_name")] + event.get("data_path"),
                value=event.get("data_value"),
                data=self.session_data,
            )
        if event.get("api_command"):
            self.session_data = self.execute_command(
                session_data=self.session_data, socket=self.__socket__, command=event.get("api_command")
            )
                
    def validate(self):
        """
        Validate the current session data against the cave_utils Validator.

        Prints and/or raises based on `print_on_invalid` and `raise_on_invalid` flags set at init time.
        """
        validator = Validator(self.session_data, ignore_keys=self.__ignore_keys__)
        if validator.log.log:
            if self.__print_on_invalid__:
                validator.log.print_logs()
            if self.__raise_on_invalid__:
                raise Exception(f"Session data validation failed. Last executed event: {self.events[self.__current_step__]}")


    def advance(self, num_steps:int|Literal['all']=1, validate_each_step:bool=False, validate_on_completion:bool=True):
        """
        Execute one or more events from the log in sequence.

        The first call initializes session data via `execute_command("init")`;
        subsequent calls apply recorded mutations and commands on top of it.

        Optional:

        - `num_steps`:
            - Type: int | "all"
            - What: Number of events to advance, or `"all"` to replay every remaining event in the log
            - Default: 1
        - `validate_each_step`:
            - Type: bool
            - What: Whether to run the validator after every individual event
            - Default: False
            - Note: Slower but pinpoints exactly which event produces invalid state
        - `validate_on_completion`:
            - Type: bool
            - What: Whether to run the validator once after all requested steps complete
            - Default: True
            - Note: Ignored when `validate_each_step` is True since validation already ran per step
        """
        if num_steps == 'all':
            num_steps = len(self.events) - self.__current_step__ - 1
        if self.__current_step__ + num_steps >= len(self.events):
            raise ValueError(f"Cannot advance {num_steps} steps from current step {self.__current_step__} because it would exceed the total number of events {len(self.events)}.")
        steps_advanced = 0
        while steps_advanced < num_steps and self.__current_step__ + 1 < len(self.events):
            # Initialize session data if this is the first time advance is called
            if self.session_data is None:
                self.session_data = self.execute_command(session_data={}, socket=self.__socket__, command="init")
            else:
                self.__execute_step__()
            self.__current_step__ += 1
            steps_advanced += 1
            if validate_each_step:
                self.validate()
        if validate_on_completion and not validate_each_step:
            self.validate()

    def get_path(self, path:list[str]):
        """
        Return the value at a nested path within the current session data.

        Requires:

        - `path`:
            - Type: list[str]
            - What: The nested key path to retrieve from `session_data`
        """
        return pamda.path(path, self.session_data)

    def print_path(self, path:list[str]):
        """
        Print the value at a nested path within the current session data.

        Requires:

        - `path`:
            - Type: list[str]
            - What: The nested key path to retrieve and print from `session_data`
        """
        value = self.get_path(path)
        print(f"{path}: {value}")