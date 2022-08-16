from functools import reduce
from scoptimize.network import (
    Model as SCModel,
    Node as SCNode,
    Flow as SCFlow,
)


def pathOr(or_val, path, data):
    """
    Takes in a nested dictionary (data) and returns the value at the end of a specified path.

    Requires:

        - `or_val`:
            - Type: any
            - What: The value to be returned if the path does not exist in data
        - `path`:
            - Type: list of strs
            - What: The path at which to look for a value
        - `data`:
            - Type: nested dictionary (n levels)
            - What: A nested dicitonary on which to coduct a function
    """
    return reduce(lambda x, y: x.get(y, {}), path[:-1], data).get(path[-1], or_val)


def assocPath(path, value, data):
    """
    Takes in a nested dictionary (data) and assigns a value to it the end of a path

    Requires:

        - `path`:
            - Type: list of strs
            - What: The path at which to assign a value
        - `value`:
            - Type: any
            - What: The value to be assigned to the end of the path
        - `data`:
            - Type: nested dictionary (n levels)
            - What: A nested dicitonary on which to coduct a function
    """
    if len(path) > 0:
        data[path[0]] = assocPath(path[1:], value, data[path[0]])
    else:
        data = value
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
        return pathOr(default, [key, "value"], self.props)

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

        # Custom init variables depending on model object type
        if self.type in ["transport", "last_mile"]:
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
                "transportation"
                if self.type in ["transport", "last_mile"]
                else self.type: [self.id],
            },
            "values": values,
        }

    def get_outputs(self):
        self.model_object.get_stats()

        # Get statistics helpers
        if self.type in ["factory", "warehouse"]:
            units_processed_key = "outflows"
        elif self.type in ["demand"]:
            units_processed_key = "inflows"
        else:
            units_processed_key = "flow"

        units_processed = self.model_object.stats.get(units_processed_key, 0)
        variable_cashflow = self.model_object.stats.get("variable_cashflow", 0)
        total_cashflow = variable_cashflow + self.fixed_cashflow

        self.props.set_prop(key="output_total_units", value=units_processed)
        self.props.set_prop(key="output_total_variable_cashflow", value=variable_cashflow)
        self.props.set_prop(key="output_total_fixed_cashflow", value=self.fixed_cashflow)

        # Get appropriate stats data values given the object type
        self.stat_values = {
            "total_cashflow": total_cashflow,
        }
        if self.type == "demand":
            self.stat_values.update(
                {
                    "demand": self.processing_capacity,
                    "demand_met": units_processed,
                    "revenue": total_cashflow,
                }
            )
        else:
            self.stat_values.update(
                {
                    "total_cashflow": total_cashflow,
                    "units_processed": units_processed,
                    "processing_cashflow": variable_cashflow,
                    "processing_capacity": self.processing_capacity,
                    "total_costs": total_cashflow,
                }
            )
            if self.type in ["warehouse", "factory"]:
                self.stat_values.update({"fixed_cashflow": self.fixed_cashflow})
        self.stats_data = self.format_stats_data(self.stat_values)

    def add_to_model(self, model):
        if self.type in ["last_mile", "transport"]:
            self.model_object = SCFlow(
                name=f"{self.id}",
                start=f"{self.origin_id}",
                end=f"{self.destination_id}",
                cashflow_per_unit=self.cashflow_per_unit,
                max_units=self.processing_capacity,
            )
        if self.type in ["demand", "factory", "warehouse"]:
            self.model_object = SCNode(
                name=f"{self.id}",
                destination=self.type == "demand",
                origin=self.type == "factory",
                cashflow_per_unit=self.cashflow_per_unit,
                max_units=self.processing_capacity,
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
            "transport": "arcs",
            "last_mile": "arcs",
            "factory": "nodes",
            "warehouse": "nodes",
            "demand": "geos",
        }

    def session_path(self, path, default=None):
        return pathOr(default, path, self.session_data)

    def get_model_objects(self, data_key):
        return {
            key: Model_Object(id=key, item=value)
            for key, value in self.session_path([data_key, "data"]).items()
        }

    def get_kpis(self):
        open_factories = [i for i in self.model_objects.values() if i.type == "factory" and i.open]
        open_warehouses = [
            i for i in self.model_objects.values() if i.type == "warehouse" and i.open
        ]
        demand_zones = [i for i in self.model_objects.values() if i.type == "demand"]
        transportation = [
            i for i in self.model_objects.values() if i.type in ["transport", "last_mile"]
        ]

        # KPIs
        self.kpis = {
            # Factories
            "num_open_factories": len(open_factories),
            "factory_units_processed": self.get_agg_stat_sum(
                model_object_list=open_factories,
                key="units_processed",
            ),
            "factory_processing_costs": self.get_agg_stat_sum(
                model_object_list=open_factories,
                key="processing_cashflow",
            ),
            "factory_fixed_costs": self.get_agg_stat_sum(
                model_object_list=open_factories,
                key="fixed_cashflow",
            ),
            "factory_processing_utilization": self.get_agg_stat_div(
                model_object_list=open_factories,
                numerator_key="units_processed",
                denominator_key="processing_capacity",
            )
            * 100,
            # Warehouses
            "num_open_warehouses": len(open_warehouses),
            "warehouse_units_processed": self.get_agg_stat_sum(
                model_object_list=open_warehouses,
                key="units_processed",
            ),
            "warehouse_processing_costs": self.get_agg_stat_sum(
                model_object_list=open_warehouses,
                key="processing_cashflow",
            ),
            "warehouse_fixed_costs": self.get_agg_stat_sum(
                model_object_list=open_warehouses,
                key="fixed_cashflow",
            ),
            "warehouse_processing_utilization": self.get_agg_stat_div(
                model_object_list=open_warehouses,
                numerator_key="units_processed",
                denominator_key="processing_capacity",
            )
            * 100,
            # Transportation
            "total_transportation_costs": self.get_agg_stat_sum(
                model_object_list=transportation,
                key="processing_cashflow",
            ),
            # Demand Zones
            "total_demand": self.get_agg_stat_sum(
                model_object_list=demand_zones,
                key="demand",
            ),
            "total_demand_met": self.get_agg_stat_sum(
                model_object_list=demand_zones,
                key="demand_met",
            ),
            "pct_total_demand_met": self.get_agg_stat_div(
                model_object_list=demand_zones,
                numerator_key="demand_met",
                denominator_key="demand",
            )
            * 100,
            "revenue": self.get_agg_stat_sum(
                model_object_list=demand_zones,
                key="revenue",
            ),
        }
        self.kpis.update(
            {
                "total_revenue": self.kpis["revenue"],
                "total_processing_costs": sum(
                    [value for key, value in self.kpis.items() if "processing_cost" in key]
                ),
                "total_fixed_costs": sum(
                    [value for key, value in self.kpis.items() if "fixed_cost" in key]
                ),
                "total_costs": sum([value for key, value in self.kpis.items() if "cost" in key]),
            }
        )
        # Update KPIs
        self.kpis.update({"total_profit": self.kpis["revenue"] + self.kpis["total_costs"]})

    def update_kpis(self):
        for key, value in self.kpis.items():
            self.session_data["kpis"]["data"][key]["value"] = value

    def clear_stats_data(self):
        self.session_data["stats"]["data"] = {}

    def add_to_stats_data(self, model_object):
        self.session_data["stats"]["data"][model_object.id] = model_object.stats_data

    def update_prop_ranges(self):
        for object_type in ["transport", "last_mile", "factory", "warehouse", "demand"]:
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
        self.get_kpis()
        self.update_kpis()
        # Update prop ranges
        self.update_prop_ranges()

        # Return modified session_data
        return self.session_data
