from cave_api.serialization_model.serialize import get_api_object
from pprint import pprint as print
from functools import reduce


def getPathValue(path, data, default=None):
    """
    Takes in a nested dictionary (data) and returns the value at the end of a specified path (a list of keys of the nested structure).

    Requires:
        - `path`:
            - Type: list of strs
            - What: The path at which to look for a value
        - `data`:
            - Type: nested dictionary (n levels)
            - What: The nested dictionary to look through
    Optional:
        - `else_val`:
            - Type: any
            - What: The value to be returned if the path does not exist in data
    """
    return reduce(lambda x, y: x.get(y, {}), path[:-1], data).get(path[-1], default)


def setPathValue(path, value, data):
    """
    Takes in a nested dictionary (data), sets the value of the last key in the path, and returns the data. If the last key in the path doesn't already exist, creates a new key-value pair and adds it to the dictionary.

    Requires:
        - `path`:
            - Type: list of strs
            - What: The path at which to assign a value
        - `data`:
            - Type: nested dictionary (n levels)
            - What: The nested dictionary to look through
        - `value`:
            - Type: any
            - What: The value to be assigned to the end of the path
    """
    if len(path) == 1:
        data[path[0]] = value
    else:
        data[path[0]] = setPathValue(path[1:], value, data[path[0]])
    return data


def flatten(data):
    """
    Takes in a list of lists (data) and returns an aggregate list of all items in all lists

    Requires:

        - `data`:
            - Type: list of lists
            - What: A list of lists on which to conduct a function

    Example:

    ```
    flatten([[1,2,3],[4,5,6]]) #=> [1,2,3,4,5,6]
    ```
    """
    return reduce(lambda x, y: x + y, data, [])


def dictMerge(data):
    """
    Takes in a list of dictionaries (data) and aggregates values for similar keys into a list

    Requires:

        - `data`:
            - Type: list of dicts
            - What: A list of dictionaries on which to conduct a function

    Example:

    ```
    dictMerge([{'a':1},{'a':2,'b':2}]) #=> {'a': [1, 2], 'b': [2]}
    ```
    """
    out = {}
    for i in flatten([list(obj.items()) for obj in data]):
        out[i[0]] = out.get(i[0], []) + [i[1]]
    return out


class Model_Object:
    def __init__(self, id, item):
        # General Model Object Data
        self.id = id
        self.item = item
        self.type = item.get("type")
        self.category = item.get("category", {})
        self.stat_values = {}  # custom stats data values given object types

        self.props = item.get("props", {})
        self.numeric_props = [
            key
            for key, value in self.props.items()
            if isinstance(value.get("value"), (int, float))
            and not isinstance(value.get("value"), bool)
        ]
        self.clear_outputs()

    def clear_outputs(self):
        """Set all numeric keys in self.props to 0 if the key in self.props includes `output`"""
        for key in self.numeric_props:
            if "output" in key:
                self.set_prop(key, 0)

    def get_prop(self, key, default=None):
        """
        Gets a prop value from the self.props object

        Requires:
            - `key`:
                - Type: str
                - What: The key for the prop value to be fetched

        Optional:
            - `default`:
                - Type: any
                - What: The default value to be used if no value is found for the given key
        """
        return getPathValue([key, "value"], self.props)

    def set_prop(self, key, value):
        """
        Associates a prop value to a prop given a key. If key doesn't already exist, create a new key-value pair and adds it to self.props. Updates self.numeric_props.

        Requires:
            - `key`:
                - Type: str
                - What: The key at which to associate the prop value
            - `value`:
                - Type: any
                - What: The value to be assigned to the prop
                - Note: The type should match the type necessary as specified in the prop itself
        """
        if self.get_prop(key) is not None:
            setPathValue([key, "value"], value, self.props)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                if key in self.numeric_props:
                    self.numeric_props.remove(key)
        else:
            setPathValue([key], {"value": value}, self.props)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            self.numeric_props.append(key)

    def get_numeric_prop_values(self):
        """
        Fetches all numeric prop values from self.props as a dictionary of key and values such that the `value` is the prop value and not the prop dictionary
        """
        return {key: self.get_prop(key, 0) for key in self.numeric_props}


class Aggregate_Serializer:
    def get_agg_stat_sum(self, model_object_list, key, round_to=2):
        return round(sum([i.stat_values.get(key, 0) for i in model_object_list]), round_to)

    def get_agg_stat_div(
        self, model_object_list, numerator_key, denominator_key, percentage=False, round_to=2
    ):
        return round(
            (
                sum([i.stat_values.get(numerator_key, 0) for i in model_object_list])
                / max(sum([i.stat_values.get(denominator_key, 0) for i in model_object_list]), 1)
            )
            * (100 if percentage else 1),
            round_to,
        )

    def get_max_and_min_dict(self, prop_list, force_int=True, flippable=True):
        max_val = max(prop_list + [0])
        min_val = min(prop_list + [0])
        if flippable:
            if max_val <= 0 and min_val < 0:
                min_val, max_val = max_val, min_val
        if force_int:
            max_val = int(max_val)
            min_val = int(min_val)
        return {"min": min_val, "max": max_val}

    def get_agg_prop_ranges(self, model_object_list, round_to=2):
        prop_lists = dictMerge([i.get_numeric_prop_values() for i in model_object_list])
        return {key: self.get_max_and_min_dict(value) for key, value in prop_lists.items()}


# Example: getting aggregate prop ranges for node 1 and node 2
example = get_api_object()
node_1 = Model_Object("node_1", getPathValue(["nodes", "data", "node_1"], example))
node_2 = Model_Object("node_2", getPathValue(["nodes", "data", "node_2"], example))
solver = Aggregate_Serializer()
print(solver.get_agg_prop_ranges([node_1, node_2]))
