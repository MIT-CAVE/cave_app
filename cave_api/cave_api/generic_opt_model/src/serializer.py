import type_enforced
from pamda import pamda
from .config import (
    data_location,
    product_unit,
    money_unit,
    currency_format,
    percent_format,
    product_format,
    node_types,
    node_geo_types,
    arc_types,
    geo_types,
    all_types,
    total_type_keys,
    destination_type_keys,
)


class Location:
    @type_enforced.Enforcer
    def __init__(self, id: str, continent: str, country: str, region: str):
        self.id = id
        self.continent = continent
        self.country = country
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
        open: bool,
        geoId: [None, str, int],
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
        self.types = node_geo_types
        self.open = open
        self.geoId = geoId
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
        return self.types[self.type]["name"]

    def validate(self):
        assert self.type in self.types.keys(), f"Unsupported Node type: {self.type}"
        assert (
            self.processing_capacity >= 0
        ), "processing capacity should always be greater than or equal to 0"

    def serialize(self):
        extra_args = {"geoJsonValue": self.geoId} if self.geoId else {}
        return {
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "type": self.type,
            "category": {
                "location": [self.location.id],
            },
            **extra_args,
            "location_id": self.location.id,
            "props": {
                "variables": {},
                "processing_capacity": {"value": self.processing_capacity},
                "cashflow_per_unit": {"value": self.processing_cashflow_per_unit},
                "outputs": {},
                "output_total_units": {"value": 0},
                "output_processing_capacity_utilization": {"value": 0},
                "output_total_variable_cashflow": {"value": 0},
                "fixed_cashflow": {"value": self.fixed_cashflow},
                "open": {"value": self.open},
                "output_total_fixed_cashflow": {"value": 0},
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
        nodes_and_geos,
    ):
        self.id = id
        self.type = type
        self.origin = nodes_and_geos[origin]
        self.destination = nodes_and_geos[destination]
        self.processing_cashflow_per_unit = processing_cashflow_per_unit
        self.processing_capacity = processing_capacity
        self.name = f"{self.origin.name} -> {self.destination.name}"
        self.location = self.origin.location
        self.types = arc_types
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
        return self.types[self.type]["name"]

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
                "output_processing_capacity_utilization": {"value": 0},
                "output_total_variable_cashflow": {"value": 0},
            },
        }


class Serializer:
    def __init__(self):
        self.locations = {
            i["id"]: Location(**i)
            for i in pamda.read_csv(data_location + "locations.csv", cast_items=True)
        }
        self.nodes = {
            i["id"]: Node(**i, locations=self.locations)
            for i in pamda.read_csv(data_location + "nodes.csv", cast_items=True)
            if i["type"] in node_types.keys()
        }
        self.geos = {
            i["id"]: Node(**i, locations=self.locations)
            for i in pamda.read_csv(data_location + "nodes.csv", cast_items=True)
            if i["type"] in geo_types.keys()
        }
        nodes_and_geos = {**self.nodes, **self.geos}
        self.arcs = {
            i["id"]: Arc(**i, nodes_and_geos=nodes_and_geos)
            for i in pamda.read_csv(data_location + "arcs.csv", cast_items=True)
        }
        self.node_data = {key: self.get_items_of_type(self.nodes, key) for key in node_types.keys()}
        self.geo_data = {key: self.get_items_of_type(self.geos, key) for key in geo_types.keys()}
        self.arc_data = {key: self.get_items_of_type(self.arcs, key) for key in arc_types.keys()}

    def get_items_of_type(self, obj_dict, obj_type):
        return {key: value for key, value in obj_dict.items() if value.type == obj_type}

    def get_categories_item_data(self, items_dict, additional_key_fn_dict={}):
        out = {}
        for key, value in items_dict.items():
            out[key] = {
                "item": value.name,
                **{fn_key: fn(value) for fn_key, fn in additional_key_fn_dict.items()},
            }
        return out

    def get_categories_location_data(self):
        return {
            i.id: {"continent": i.continent, "country": i.country, "region": i.region}
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
            "output_processing_capacity_utilization": {
                "name": "Processing Capacity Utilization",
                "type": "num",
                "value": 0,
                "enabled": False,
                "help": "The percentage of processing capacity used by this network object after running this model",
                "numberFormat": percent_format,
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
            "numColumns": 2,
            "numRows": 5,
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
                    "itemId": "output_processing_capacity_utilization",
                },
                "col2_row4": {
                    "type": "item",
                    "column": 2,
                    "row": 4,
                    "itemId": "output_total_variable_cashflow",
                },
                "col2_row5": {
                    "type": "item",
                    "column": 2,
                    "row": 5,
                    "itemId": "output_total_fixed_cashflow",
                },
            },
        }
        return {
            "type": "grid",
            "numColumns": 2,
            "numRows": 3,
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
                    "itemId": "output_processing_capacity_utilization",
                },
                "col2_row4": {
                    "type": "item",
                    "column": 2,
                    "row": 4,
                    "itemId": "output_total_variable_cashflow",
                },
            },
        }

    def get_dropdown_options(self, items_dict, include_categorical=False):
        try:
            return list(items_dict.values())[0].get_dropdown_options(include_categorical)
        except:
            return []

    def get_kpi_data_template(self):
        out = {}
        for key, value in all_types.items():
            out.update(
                {
                    f"{key}_header": {
                        "name": f"{value['name_singular']} KPIs",
                        "icon": value["icon"],
                        "type": "head",
                        "value": 0,
                    },
                    f"{key}_count_used": {
                        "name": f"{value['name_singular']+' '+value.get('kpi_count_units') if value.get('kpi_count_units') else value['name']} Used",
                        "value": 0,
                        "numberFormat": {
                            "precision": 0,
                        },
                        "icon": "AiOutlineNumber",
                    },
                    f"{key}_units_processed": {
                        "name": f"{value['name_singular']} {'Demand Met' if key in total_type_keys+destination_type_keys else 'Units Processed'}",
                        "value": 0,
                        "numberFormat": product_format,
                        "icon": "FaBox",
                    },
                    f"{key}_processing_cashflows": {
                        "name": f"{value['name_singular']} Processing Cashflows",
                        "value": 0,
                        "numberFormat": currency_format,
                        "icon": "FaMoneyBill",
                    },
                    f"{key}_fixed_cashflows": {
                        "name": f"{value['name_singular']} Fixed Cashflows",
                        "value": 0,
                        "numberFormat": currency_format,
                        "icon": "FaMoneyBill",
                    },
                    f"{key}_total_cashflows": {
                        "name": f"{value['name_singular']} Cashflows (Total)",
                        "value": 0,
                        "numberFormat": currency_format,
                        "icon": "FaMoneyBill",
                    },
                    f"{key}_processing_utilization": {
                        "name": f"{value['name_singular']} {'Percent Demand Met' if key in total_type_keys+destination_type_keys else 'Processing Utilization'}",
                        "value": 0,
                        "percentage": True,
                        "numberFormat": {
                            "unit": f"%",
                            "unitSpace": False,
                            "precision": 0,
                        },
                        "icon": "MdDataUsage",
                    },
                }
            )
        return out

    def get_kpi_layout_template(self):
        out = {}
        row = 0
        for key, value in all_types.items():
            row += 2 if key in total_type_keys else 1
            for col, item in enumerate(
                [
                    f"{key}_header",
                    f"{key}_count_used",
                    f"{key}_units_processed",
                    f"{key}_processing_cashflows",
                    f"{key}_fixed_cashflows",
                    f"{key}_total_cashflows",
                    f"{key}_processing_utilization",
                ]
            ):
                out.update(
                    {
                        f"row{row}_col{col+1}": {
                            "type": "item",
                            "itemId": item,
                            "column": col + 1,
                            "row": row,
                        },
                    }
                )

        values = list(out.values())
        return {
            "type": "grid",
            "numColumns": max(pamda.pluck(["column"], list(out.values()))),
            "numRows": max(pamda.pluck(["row"], list(out.values()))),
            "data": out,
        }

    def get_stats_types(self):
        return {
            "processing_capacity": {
                "name": "Processing Capacity",
                "calculation": "processing_capacity",
                "numberFormat": currency_format,
                "order": 0,
            },
            "units_processed": {
                "name": "Units Processed",
                "calculation": "units_processed",
                "numberFormat": product_format,
                "order": 1,
            },
            "processing_capacity_utilization": {
                "name": "Processing Capacity Utilization",
                "calculation": "units_processed / groupSum('processing_capacity') * 100",
                "numberFormat": percent_format,
                "order": 2,
            },
            "processing_cashflow": {
                "name": "Processing Cashflow",
                "calculation": "processing_cashflow",
                "numberFormat": currency_format,
                "order": 3,
            },
            "fixed_cashflow": {
                "name": "Fixed Cashflow",
                "calculation": "fixed_cashflow",
                "numberFormat": currency_format,
                "order": 4,
            },
            "cashflow": {
                "name": "Total Cashflow",
                "calculation": "total_cashflow",
                "numberFormat": {"unit": f"{money_unit}", "currency": True},
                "order": 5,
            },
        }
