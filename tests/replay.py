from utils.replay import Replay
import os

LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutation_logs")


def test_replay(log_file):
    # Create a Replay instance for the given log file
    replay = Replay(mutation_log_file=log_file, print_on_invalid=True, raise_on_invalid=True)

    # Advance through all steps without intermediate validation or final validation
    replay.advance(num_steps='all', validate_each_step=False, validate_on_completion=False)

    # Manually trigger validation after replaying all steps
    replay.validate()

    # Example: Validate that some path is valid:
    iconUrl = replay.get_path(['settings', 'iconUrl'])
    assert iconUrl == "https://react-icons.mitcave.com/5.4.0", f"Expected iconUrl to be 'https://react-icons.mitcave.com/5.4.0', but got {iconUrl}"
    
    # Example: Print the value at some path
    replay.print_path(['settings', 'iconUrl'])


def test_all_logs():
    for log_file in os.listdir(LOGS_DIR):
        print(f"Testing replay for log file: {log_file}")
        test_replay(log_file=os.path.join(LOGS_DIR, log_file))
        print(f"Successfully tested replay for log file: {log_file}\n")


if __name__ == "__main__":
    test_replay(log_file=os.path.join(LOGS_DIR, "MutationLogExample.csv"))
    # test_all_logs()
