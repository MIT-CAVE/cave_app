from functools import reduce


def get_force_dict(object, key):
    """
    Code from Pamda: https://github.com/connor-makowski/pamda
    - Returns a value from a dictionary given a key and forces that value to be a dictionary
    - Note: This updates the object in place to force the value from the key to be a dictionary

    Requires:

    - `object`:
        - Type: dict | list
        - What: The object from which to look for a key
    - `key`:
        - Type: str
        - What: The key to look up in the object
    ```
    """
    if not isinstance(object.get(key), (dict, list)):
        object.__setitem__(key, {})
    return object.get(key)


def assoc_path(path, value, data):
    """
    Code from Pamda: https://github.com/connor-makowski/pamda

    - Ensures a path exists within a nested dictionary

    Requires:

    - `path`:
        - Type: list of strs | str
        - What: The path to check
        - Note: If a string is passed, assumes a single item path list with that string
    - `value`:
        - Type: any
        - What: The value to appropriate to the end of the path
    - `data`:
        - Type: dict
        - What: A dictionary in which to associate the given value to the given path
    """
    if isinstance(path, str):
        path = [path]
    reduce(get_force_dict, path[:-1], data).__setitem__(path[-1], value)
    return data
