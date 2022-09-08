import type_enforced
import csv
import pkg_resources

# For Pip based package resources see:
# https://stackoverflow.com/questions/779495/access-data-in-package-subdirectory
data_location = pkg_resources.resource_filename("cave_api", "simple_model/data/")
product_unit = "unit"
money_unit = "$"
currency_format = {
    "precision": 2,
    "unit": f"{money_unit}",
    "currency": True,
}
percent_format = {
    "unit": "%",
    "unitSpace": False,
}
product_format = {
    "precision": 0,
    "unit": f"{product_unit}s",
}


def cast_number(string):
    try:
        float_string = float(string)
        return int(float_string) if float_string == int(float_string) else float_string
    except:
        return string


def read_csv(filename):
    with open(filename) as f:
        file_data = csv.reader(f)
        headers = next(file_data)
        return [dict(zip(headers, map(cast_number, i))) for i in file_data]


class Location:
    @type_enforced.Enforcer
    def __init__(self, id: str, continent: str, region: str):
        self.id = id
        self.continent = continent
        self.region = region


class Node:
    @type_enforced.Enforcer
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        fixed_cashflow: [int, float],
        processing_cashflow_per_unit: [int, float],
        processing_capacity: [int, float],
        latitude: [int, float],
        longitude: [int, float],
        altitude: [int, float],
        location: str,
        geoId: str,
        locations,
    ):
        self.id = id
        self.type = type
        self.name = name
        self.fixed_cashflow = fixed_cashflow
        self.processing_cashflow_per_unit = processing_cashflow_per_unit
        self.processing_capacity = processing_capacity
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.location = locations[location]
        self.geoId = geoId
        self.types = {
            "factory": "Factories",
            "demand": "Demand Zones",
            "warehouse": "Warehouses",
        }
        self.validate()
        self.serialized_data = self.serialize()

    def get_dropdown_option_data(self, prop_dict):
        if isinstance(prop_dict.get("value"), bool):
            return {"false": "rgb(255,0,0)", "true": "rgb(0,255,0)"}
        else:
            return {
                "min": 0,
                "max": 0,
                "startGradientColor": {
                    "dark": "rgb(255, 136, 136)",
                    "light": "rgb(187, 0, 0)",
                },
                "endGradientColor": {
                    "dark": "rgb(176, 255, 110)",
                    "light": "rgb(58, 131, 0)",
                },
            }

    def get_dropdown_options(self, include_categorical=False):
        options = {
            prop: self.get_dropdown_option_data(prop_dict)
            for prop, prop_dict in self.serialized_data["props"].items()
            if "value" in prop_dict
            and (include_categorical or not isinstance(prop_dict.get("value"), bool))
        }
        return dict(sorted(options.items()))

    def get_pretty_type(self):
        return self.types[self.type]

    def validate(self):
        assert self.type in self.types.keys(), f"Unsupported Node type: {self.type}"
        assert (
            self.processing_capacity >= 0
        ), "processing capacity should always be greater than or equal to 0"
        if self.type == "demand":
            assert (
                self.processing_cashflow_per_unit >= 0
            ), f"processing_cashflow_per_unit should be greater than or equal to 0 for {self.type} nodes."
            assert self.geoId != None, f"geoId must be specified for {self.type} nodes."
        else:
            assert (
                self.processing_cashflow_per_unit <= 0
            ), f"processing_cashflow_per_unit should be less than or equal to 0 for {self.type} nodes."
            assert (
                self.geoId == ""
            ), f"geoId must not be specified for {self.type} nodes."
            assert (
                self.fixed_cashflow <= 0
            ), f"fixed_cashflow should be less than or equal to 0 for {self.type} type nodes"

    def serialize(self):
        if self.type == "demand":
            extra_props = {}
            extra_keys = {
                "geoJsonValue": self.geoId,
            }
        else:
            extra_props = {
                "fixed_cashflow": {"value": self.fixed_cashflow},
                "open": {"value": False},
                "output_total_fixed_cashflow": {"value": 0},
            }
            extra_keys = {}
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "type": self.type,
            "category": {
                "location": [self.location.id],
            },
            "location_id": self.location.id,
            **extra_keys,
            "props": {
                "variables": {},
                "processing_capacity": {"value": self.processing_capacity},
                "cashflow_per_unit": {"value": self.processing_cashflow_per_unit},
                "outputs": {},
                "output_total_units": {"value": 0},
                "output_total_variable_cashflow": {"value": 0},
                **extra_props,
            },
        }


class Arc:
    @type_enforced.Enforcer
    def __init__(
        self,
        id: str,
        type: str,
        origin: str,
        destination: str,
        processing_cashflow_per_unit: [int, float],
        processing_capacity: [int, float],
        nodes,
    ):
        self.id = id
        self.type = type
        self.origin = nodes[origin]
        self.destination = nodes[destination]
        self.processing_cashflow_per_unit = processing_cashflow_per_unit
        self.processing_capacity = processing_capacity
        self.name = f"{self.origin.name} -> {self.destination.name}"
        self.location = self.origin.location
        self.types = {
            "transport": "Transport",
            "last_mile": "Last Mile",
        }
        self.validate()

        self.serialized_data = self.serialize()

    def get_dropdown_option_data(self, prop_dict):
        if isinstance(prop_dict.get("value"), bool):
            return {"false": "rgb(255,0,0)", "true": "rgb(0,255,0)"}
        else:
            return {
                "min": 0,
                "max": 0,
                "startGradientColor": {
                    "dark": "rgb(255, 136, 136)",
                    "light": "rgb(187, 0, 0)",
                },
                "endGradientColor": {
                    "dark": "rgb(176, 255, 110)",
                    "light": "rgb(58, 131, 0)",
                },
            }

    def get_dropdown_options(self, include_categorical=False):
        options = {
            prop: self.get_dropdown_option_data(prop_dict)
            for prop, prop_dict in self.serialized_data["props"].items()
            if "value" in prop_dict
            and (include_categorical or not isinstance(prop_dict.get("value"), bool))
        }
        return dict(sorted(options.items()))

    def get_pretty_type(self):
        return self.types[self.type]

    def validate(self):
        assert self.type in self.types.keys(), f"Unsupported Arc type: {self.type}"
        assert (
            self.processing_cashflow_per_unit <= 0
        ), "processing_cashflow_per_unit should be less than or equal to 0"
        assert (
            self.processing_capacity >= 0
        ), "processing capacity should be greater than or equal to 0"

    def serialize(self):
        return {
            "name": self.name,
            "startLatitude": self.origin.latitude,
            "startLongitude": self.origin.longitude,
            "startAltitude": self.origin.altitude,
            "endLatitude": self.destination.latitude,
            "endLongitude": self.destination.longitude,
            "endAltitude": self.destination.altitude,
            "type": self.type,
            "category": {
                "location": [
                    self.origin.location.id,
                    self.destination.location.id,
                ],
            },
            "origin_id": self.origin.id,
            "destination_id": self.destination.id,
            "location_id": self.location.id,
            "props": {
                "variables": {},
                "processing_capacity": {"value": self.processing_capacity},
                "cashflow_per_unit": {"value": self.processing_cashflow_per_unit},
                "outputs": {},
                "output_total_units": {"value": 0},
                "output_total_variable_cashflow": {"value": 0},
            },
        }


class Serializer:
    def __init__(self):
        self.locations = {
            i["id"]: Location(**i) for i in read_csv(data_location + "locations.csv")
        }
        self.nodes = {
            i["id"]: Node(**i, locations=self.locations)
            for i in read_csv(data_location + "nodes.csv")
        }
        self.arcs = {
            i["id"]: Arc(**i, nodes=self.nodes)
            for i in read_csv(data_location + "arcs.csv")
        }
        self.warehouses = {
            key: value
            for key, value in self.nodes.items()
            if value.type in ["warehouse"]
        }
        self.factories = {
            key: value for key, value in self.nodes.items() if value.type in ["factory"]
        }
        self.demand_zones = {
            key: value for key, value in self.nodes.items() if value.type in ["demand"]
        }

    def get_categories_item_data(self, items_dict, **kwargs):
        return {
            key: {
                "type": value.get_pretty_type(),
                "continent": value.location.continent,
                "item": value.name,
                **kwargs,
            }
            for key, value in items_dict.items()
        }

    def get_categories_location_data(self):
        return {
            i.id: {"continent": i.continent, "region": i.region}
            for i in self.locations.values()
        }

    def get_serialized_item_data(self, items_dict):
        return {key: value.serialized_data for key, value in items_dict.items()}

    def get_general_prop_defaults(self):
        return {
            "variables": {
                "name": "Input Variables",
                "type": "head",
                "help": "Input variables used for the model.",
            },
            "processing_capacity": {
                "name": "Processing Capacity",
                "type": "num",
                "enabled": True,
                "help": f"The baseline processing capacity for this arc or node",
                "numberFormat": product_format,
            },
            "cashflow_per_unit": {
                "name": "Processing Cost Per Unit",
                "type": "num",
                "enabled": True,
                "help": f"The processing cost per {product_unit} to flow through this arc or node",
                "numberFormat": {
                    "unit": f"{money_unit}/{product_unit}",
                },
            },
            "fixed_cashflow": {
                "name": "Fixed Cost",
                "type": "num",
                "enabled": True,
                "help": "The fixed cost to open this node",
                "numberFormat": currency_format,
            },
            "open": {
                "name": "Open",
                "type": "toggle",
                "enabled": True,
                "help": "Should this node be opened / used?",
                "value": True,
            },
            "outputs": {
                "name": "Output Totals",
                "type": "head",
                "help": "Output totals from the model",
            },
            "output_total_units": {
                "name": "Total Units Processed",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The total number of units processed for this arc or node after running this model",
                "numberFormat": product_format,
            },
            "output_total_variable_cashflow": {
                "name": "Total Processing Cost",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The total incurred processing cost for this arc or node after running this model",
                "numberFormat": currency_format,
            },
            "output_total_fixed_cashflow": {
                "name": "Total Fixed Cost",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The incurred fixed cost for this arc or node after running this model",
                "numberFormat": currency_format,
            },
        }

    def get_general_prop_layout(self):
        return {
            "type": "grid",
            "num_columns": 2,
            "num_rows": 5,
            "data": {
                "col1_row1": {
                    "type": "item",
                    "column": 1,
                    "row": 1,
                    "itemId": "variables",
                },
                "col1_row2": {
                    "type": "item",
                    "column": 1,
                    "row": 2,
                    "itemId": "processing_capacity",
                },
                "col1_row3": {
                    "type": "item",
                    "column": 1,
                    "row": 3,
                    "itemId": "cashflow_per_unit",
                },
                "col1_row4": {
                    "type": "item",
                    "column": 1,
                    "row": 4,
                    "itemId": "fixed_cashflow",
                },
                "col1_row5": {
                    "type": "item",
                    "column": 1,
                    "row": 5,
                    "itemId": "open",
                },
                "col2_row1": {
                    "type": "item",
                    "column": 2,
                    "row": 1,
                    "itemId": "outputs",
                },
                "col2_row2": {
                    "type": "item",
                    "column": 2,
                    "row": 2,
                    "itemId": "output_total_units",
                },
                "col2_row3": {
                    "type": "item",
                    "column": 2,
                    "row": 3,
                    "itemId": "output_total_variable_cashflow",
                },
                "col2_row4": {
                    "type": "item",
                    "column": 2,
                    "row": 4,
                    "itemId": "output_total_fixed_cashflow",
                },
            },
        }

    def get_geo_prop_defaults(self):
        return {
            "variables": {
                "name": "Input Variables",
                "type": "head",
                "help": "Input variables used for the model",
                "order": 0,
                "column": 1,
            },
            "processing_capacity": {
                "name": "Demand",
                "type": "num",
                "enabled": True,
                "help": f"The baseline demand for this demand zone",
                "order": 1,
                "column": 1,
                "numberFormat": product_format,
            },
            "cashflow_per_unit": {
                "name": f"Revenue Per {product_unit}",
                "type": "num",
                "enabled": True,
                "help": f"The revenue generated per {product_unit} when satisfying demand in this demand zone",
                "order": 2,
                "column": 1,
                "numberFormat": {
                    "unit": f"{money_unit}/{product_unit}",
                },
            },
            "outputs": {
                "name": "Output Totals",
                "type": "head",
                "help": "Output totals from the model",
                "order": 0,
                "column": 2,
            },
            "output_total_units": {
                "name": "Total Demand Filled",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The total amount of demand filled for this demand zone after running this model",
                "order": 1,
                "column": 2,
                "numberFormat": product_format,
            },
            "output_total_variable_cashflow": {
                "name": "Total Revenue",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The total revenue generated by this demand zone after running this model",
                "order": 2,
                "column": 2,
                "numberFormat": currency_format,
            },
        }

    def get_geo_prop_layout(self):
        return {
            "type": "grid",
            "num_columns": 2,
            "num_rows": 3,
            "data": {
                "col1_row1": {
                    "type": "item",
                    "column": 1,
                    "row": 1,
                    "itemId": "variables",
                },
                "col1_row2": {
                    "type": "item",
                    "column": 1,
                    "row": 2,
                    "itemId": "processing_capacity",
                },
                "col1_row3": {
                    "type": "item",
                    "column": 1,
                    "row": 3,
                    "itemId": "cashflow_per_unit",
                },
                "col2_row1": {
                    "type": "item",
                    "column": 2,
                    "row": 1,
                    "itemId": "outputs",
                },
                "col2_row2": {
                    "type": "item",
                    "column": 2,
                    "row": 2,
                    "itemId": "output_total_units",
                },
                "col2_row3": {
                    "type": "item",
                    "column": 2,
                    "row": 3,
                    "itemId": "output_total_variable_cashflow",
                },
            },
        }

    def get_dropdown_options(self, items_dict, include_categorical=False):
        try:
            return list(items_dict.values())[0].get_dropdown_options(
                include_categorical
            )
        except:
            return []

    def get_stats_types(self):
        return {
            "cashflow": {
                "name": "Cashflow",
                "calculation": "total_cashflow",
                "numberFormat": {"unit": f"{money_unit}", "currency": True},
                "order": 0,
            },
            "demand": {
                "name": "Demand",
                "calculation": "demand",
                "numberFormat": product_format,
                "order": 1,
            },
            "demand_met": {
                "name": "Demand Met",
                "calculation": "demand_met",
                "numberFormat": product_format,
                "order": 2,
            },
            "pct_demand_met": {
                "name": "Percent Demand Met",
                "calculation": "demand_met / groupSum('demand') * 100",
                "numberFormat": percent_format,
                "order": 2,
            },
            "revenue": {
                "name": "Revenue",
                "calculation": "revenue",
                "numberFormat": {"unit": f"{money_unit}", "currency": True},
                "order": 3,
            },
            "units_processed": {
                "name": "Units Processed",
                "calculation": "units_processed",
                "numberFormat": product_format,
                "order": 4,
            },
            "processing_cashflow": {
                "name": "Processing Cost",
                "calculation": "processing_cashflow",
                "numberFormat": currency_format,
                "order": 5,
            },
            "processing_capacity": {
                "name": "Processing Capacity",
                "calculation": "processing_capacity",
                "numberFormat": currency_format,
                "order": 5,
            },
            "processing_capacity_utilization": {
                "name": "Processing Capacity Utilization",
                "calculation": "units_processed / groupSum('processing_capacity') * 100",
                "numberFormat": percent_format,
                "order": 6,
            },
            "fixed_cashflow": {
                "name": "Fixed Cost",
                "calculation": "fixed_cashflow",
                "numberFormat": currency_format,
                "order": 10,
            },
            "total_costs": {
                "name": "Total Cost",
                "calculation": "total_costs",
                "numberFormat": currency_format,
                "order": 11,
            },
        }
