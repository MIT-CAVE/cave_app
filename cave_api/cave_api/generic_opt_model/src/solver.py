from scoptimize.network import (
    Model as SCModel,
    Node as SCNode,
    Flow as SCFlow,
)
from .config import (
    all_types,
    all_type_keys,
    node_type_keys,
    node_geo_type_keys,
    node_arc_geo_type_keys,
    total_type_keys,
    arc_type_keys,
    geo_type_keys,
    origin_type_keys,
    destination_type_keys,
    all_types,
)
from pamda import pamda


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
    for i in pamda.flatten([list(obj.items()) for obj in data]):
        out[i[0]] = out.get(i[0], []) + [i[1]]
    return out


class Props:
    """
    A class to handle props for various object types

    This class uses the prop dictionary (as specified by the api) for a given object (arc, node, geo ...) and allows for more pythonic access to get and modify values in that prop dictionary.
    """

    def __init__(self, props):
        """
        Initialize a props object

        Requires:

            - `props`:
                - Type: dict
                - What: The props object as specified by the api docs

        Notes:

            - The props object is the same object as the object from whence it was provided. This means that editing self.props in this class also edits the passed props object (since they are one in the same)
            - `self.clear_outputs` is called from on`self.__init__`
        """
        self.props = props
        self.numeric_keys = [
            key
            for key, value in props.items()
            if isinstance(value.get("value"), (int, float))
            and not isinstance(value.get("value"), bool)
        ]
        self.clear_outputs()

    def clear_outputs(self):
        """
        Set all numeric keys in self.props to 0 if the key in self.props includes `output`
        """
        for key in self.numeric_keys:
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
        return pamda.pathOr(default, [key, "value"], self.props)

    def set_prop(self, key, value):
        """
        Associates a prop value to a prop given a key

        Requires:

            - `key`:
                - Type: str
                - What: The key at which to associate the prop value
            - `value`:
                - Type: any
                - What: The value to be assigned to the prop
                - Note: The type should match the type necessary as specified in the prop itself

        Notes:

            - If a prop value does not exist in the prop, this method will not create a value in that prop
        """
        if self.get_prop(key) is not None:
            self.props[key]["value"] = value

    def get_numeric_prop_key_values(self):
        """
        Fetches all numeric prop values from self.props as a dictionary of key and values such that the `value` is the prop value and not the prop dictionary
        """
        return {key: self.get_prop(key, 0) for key in self.numeric_keys}


class Model_Object:
    def __init__(self, id, item):
        # General Model Object Data
        self.id = id
        self.type = item.get("type")
        self.props = Props(item.get("props", {}))
        self.location_id = item.get("location_id")

        # Custom init variables for arc types
        if self.type in arc_type_keys:
            self.origin_id = item.get("origin_id")
            self.destination_id = item.get("destination_id")

        # Model Inputs
        self.open = self.props.get_prop("open", True)
        self.fixed_cashflow = self.props.get_prop("fixed_cashflow", 0) if self.open else 0
        self.processing_capacity = self.props.get_prop("processing_capacity", 0) if self.open else 0
        self.cashflow_per_unit = self.props.get_prop("cashflow_per_unit", 0)

    def format_stats_data(self, values):
        return {
            "category": {
                "location": [self.location_id],
                "network_object": [self.id],
                self.type: [self.id],
            },
            "values": values,
        }

    def get_outputs(self):
        self.model_object.get_stats()

        # Get statistics helpers
        if self.type in destination_type_keys:
            units_processed_key = "inflows"
        elif self.type in node_geo_type_keys:
            units_processed_key = "outflows"
        else:
            units_processed_key = "flow"

        units_processed = self.model_object.stats.get(units_processed_key, 0)
        variable_cashflow = self.model_object.stats.get("variable_cashflow", 0)
        total_cashflow = variable_cashflow + self.fixed_cashflow

        # Set outputs
        self.props.set_prop(key="output_total_units", value=units_processed)
        self.props.set_prop(key="output_processing_capacity_utilization", value=pamda.safeDivide(self.processing_capacity, units_processed)*100)
        self.props.set_prop(key="output_total_variable_cashflow", value=variable_cashflow)
        self.props.set_prop(key="output_total_fixed_cashflow", value=self.fixed_cashflow)

        self.stat_values = {
            "processing_capacity": self.processing_capacity,
            "units_processed": units_processed,
            "processing_cashflow": variable_cashflow,
            "total_cashflow": total_cashflow,
        }
        if self.type in node_geo_type_keys:
            self.stat_values.update({"fixed_cashflow": self.fixed_cashflow})
        self.stats_data = self.format_stats_data(self.stat_values)

    def add_to_model(self, model):
        if self.type in arc_type_keys:
            self.model_object = SCFlow(
                name=f"{self.id}",
                start=f"{self.origin_id}",
                end=f"{self.destination_id}",
                cashflow_per_unit=self.cashflow_per_unit,
                max_units=self.processing_capacity,
            )
        else:
            additional_props = {"max_units": self.processing_capacity}
            if self.type in destination_type_keys:
                if all_types[self.type].get("mustMeetCapacity", True):
                    additional_props = {"min_units": self.processing_capacity}
            self.model_object = SCNode(
                name=f"{self.id}",
                destination=self.type in destination_type_keys,
                origin=self.type in origin_type_keys,
                cashflow_per_unit=self.cashflow_per_unit,
                **additional_props,
            )
        model.add_object(self.model_object)


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
        prop_lists = dictMerge([i.props.get_numeric_prop_key_values() for i in model_object_list])
        return {key: self.get_max_and_min_dict(value) for key, value in prop_lists.items()}


class Solver(Aggregate_Serializer):
    def __init__(self, session_data):
        self.session_data = session_data
        self.model_objects = {
            **self.get_model_objects("nodes"),
            **self.get_model_objects("geos"),
            **self.get_model_objects("arcs"),
        }
        self.object_type_data_key_serializer = {
            **{key: "nodes" for key in node_type_keys},
            **{key: "geos" for key in geo_type_keys},
            **{key: "arcs" for key in arc_type_keys},
        }

    def session_path(self, path, default=None):
        return pamda.pathOr(default, path, self.session_data)

    def get_model_objects(self, data_key):
        return {
            key: Model_Object(id=key, item=value)
            for key, value in self.session_path([data_key, "data"]).items()
        }

    def get_kpis(self):
        used_objects = [
            i for i in self.model_objects.values() if i.open
        ]
        destination_objects = [i for i in used_objects if i.type in destination_type_keys]
        self.kpis = {}
        for key, value in all_types.items():
            # Special logic to handle total type keys differently
            if key in total_type_keys:
                objects = used_objects
                units_processed_objects = destination_objects
            else:
                objects = [i for i in used_objects if i.type == key]
                units_processed_objects = objects
            self.kpis.update(
                {
                    f"{key}_count_used": len(objects),
                    f"{key}_units_processed": self.get_agg_stat_sum(
                        model_object_list=units_processed_objects,
                        key="units_processed",
                    ),
                    f"{key}_processing_cashflows": self.get_agg_stat_sum(
                        model_object_list=objects,
                        key="processing_cashflow",
                    ),
                    f"{key}_fixed_cashflows": self.get_agg_stat_sum(
                        model_object_list=objects,
                        key="fixed_cashflow",
                    ),
                    f"{key}_total_cashflows": self.get_agg_stat_sum(
                        model_object_list=objects,
                        key="total_cashflow",
                    ),
                    f"{key}_processing_utilization": self.get_agg_stat_div(
                        model_object_list=units_processed_objects,
                        numerator_key="units_processed",
                        denominator_key="processing_capacity",
                    )
                    * 100,
                }
            )

    def update_kpis(self):
        self.get_kpis()
        for key, value in self.kpis.items():
            self.session_data["kpis"]["data"][key]["value"] = value

    def clear_stats_data(self):
        self.session_data["stats"]["data"] = {}

    def add_to_stats_data(self, model_object):
        self.session_data["stats"]["data"][model_object.id] = model_object.stats_data

    def update_prop_ranges(self):
        for object_type in node_arc_geo_type_keys:
            model_obj_subset = [i for i in self.model_objects.values() if i.type == object_type]
            subset_prop_ranges = self.get_agg_prop_ranges(model_obj_subset)
            types_object = self.session_data[self.object_type_data_key_serializer.get(object_type)][
                "types"
            ][object_type]
            for key, value in subset_prop_ranges.items():
                types_object["colorByOptions"][key].update(value)
                try:
                    types_object["sizeByOptions"][key].update(value)
                except:
                    pass

    def solve(self):
        # Initialize Model
        self.model = SCModel(name="Model")
        # Add all network objects to the model
        for model_object in self.model_objects.values():
            model_object.add_to_model(self.model)
        # Solve the model
        self.model.solve()
        # Clear stats data
        self.clear_stats_data()
        # Get Outputs
        for model_object in self.model_objects.values():
            model_object.get_outputs()
            # Add model object to stats data
            self.add_to_stats_data(model_object)
        # KPIs
        self.update_kpis()
        # Update prop ranges
        self.update_prop_ranges()

        # Return modified session_data
        return self.session_data
