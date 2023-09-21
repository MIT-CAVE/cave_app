import json
from pamda import pamda
from cave_api.serialization_model.utils import drop_none


def serialize_item(item):
    out = {}
    for k, v in item.items():
        try:
            out[k] = json.loads(v)
        except:
            out[k] = v
    return out


def get_pages_data(data_dir):
    data = {}
    layout_data = drop_none(pamda.read_csv(data_dir + "/layout.csv", cast_items=True))
    for item in layout_data:
        id = item.pop("id")
        if id not in data:
            data[id] = {"pageLayout": []}
        data[id]["pageLayout"].append(serialize_item(item))
    return {"data": data}
