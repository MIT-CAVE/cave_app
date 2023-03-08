from pamda import pamda
import pkg_resources

# For Pip based package resources see:
# https://stackoverflow.com/questions/779495/access-data-in-package-subdirectory
data_location = pkg_resources.resource_filename("cave_api", "generic_opt_model/data/")

config = pamda.read_json(data_location + "config.json")

product_unit = config.get("product_unit")
money_unit = config.get("money_unit")
currency_format = config.get("currency_format")
percent_format = config.get("percent_format")
product_format = config.get("product_format")
node_types = config.get("node_types")
arc_types = config.get("arc_types")
geo_types = config.get("geo_types")
node_geo_types = {**node_types, **geo_types}
node_arc_geo_types = {**node_types, **arc_types, **geo_types}

total_types = {
    "total": {
        "name": "Totals",
        "name_singular": "Total",
        "kpi_count_units": "Network Objects",
        "icon": "MdOutlineVerified",
    }
}
all_types = {
    **node_arc_geo_types,
    **total_types,
}

arc_type_keys = list(arc_types.keys())
node_type_keys = list(node_types.keys())
geo_type_keys = list(geo_types.keys())
node_geo_type_keys = list(node_geo_types.keys())
node_arc_geo_type_keys = list(node_arc_geo_types.keys())
total_type_keys = list(total_types.keys())
all_type_keys = list(all_types.keys())

origin_type_keys = [key for key, value in node_geo_types.items() if value.get("isOrigin")]
destination_type_keys = [
    key for key, value in node_geo_types.items() if value.get("isDestination")
]
