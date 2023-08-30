import json
from pamda import pamda
from cave_api.serialization_model.utils import drop_none


def serialize_item(item):
    if item.get("color"):
        item["color"] = json.loads(item["color"])
    return item


def get_app_bar_data(data_dir):
    return {
        "data": {
            i.pop("id"): serialize_item(i)
            for i in drop_none(pamda.read_csv(data_dir + "appBar.csv", cast_items=True))
        }
    }
