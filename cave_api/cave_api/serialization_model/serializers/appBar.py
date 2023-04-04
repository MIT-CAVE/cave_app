import json
from pamda import pamda


def serialize_item(item):
    if item.get("color"):
        item["color"] = json.loads(item["color"])
    return item


def get_app_bar_data(data_dir):
    return {"data": {i.pop("id"): serialize_item(i) for i in pamda.read_csv(data_dir + "appBar.csv", cast_items=True)}}
