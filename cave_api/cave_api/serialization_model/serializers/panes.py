import json
from cave_api.serialization_model.utils import group_list
from pamda import pamda


def get_panes_data(data_dir):
    data = {i.pop("id"): i for i in pamda.read_csv(data_dir + "panes.csv", cast_items=True)}

    try:
        layout_data = group_list(pamda.read_csv(data_dir + "/layout.csv", cast_items=True), "paneId")
    except:
        layout_data = {}
    try:
        prop_data = group_list(pamda.read_csv(data_dir + "/props.csv", cast_items=True), "paneId")
    except:
        prop_data = {}
    try:
        context_data = group_list(pamda.read_csv(data_dir + "/contexts.csv", cast_items=True), "paneId")
    except:
        context_data = {}

    for key, value in prop_data.items():
        if data.get(key, False):
            data[key]["props"] = {}
            for i in value:
                prop_id, prop_dict = i.pop("propId"), {}
                for k, v in i.items():
                    try:
                        prop_dict[k] = json.loads(v)
                    except:
                        prop_dict[k] = v
                data[key]["props"][prop_id] = prop_dict

    for key, value in layout_data.items():
        if isinstance(data.get(key), dict):
            data[key]["layout"] = {
                "type": "grid",
                "numColumns": "auto",
                "numRows": "auto",
                "data": {},
            }
            for i in value:
                grid_id = f"col{i.get('column')}Row{i.get('row')}"
                data[key]["layout"]["data"][grid_id] = {
                    "type": "item",
                    "column": i.get("column"),
                    "row": i.get("row"),
                    "itemId": i.get("itemId"),
                }

    for key, value in context_data.items():
        if data.get(key, False):
            data[key]["data"] = {}
            for i in value:
                data_id = i.pop("id")
                data_dict = {}
                for k, v in i.items():
                    try:
                        data_dict[k] = json.loads(v)
                    except:
                        data_dict[k] = v
                data[key]["data"][data_id] = data_dict
    return {"data": data}
