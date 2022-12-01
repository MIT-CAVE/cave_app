import sys

if sys.version_info[0] == 3:
    from .big_model.api import execute_command
elif sys.version_info[0] < 3:
    raise Exception("This package only supports python3")
