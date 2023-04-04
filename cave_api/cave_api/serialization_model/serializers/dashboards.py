import json
from pamda import pamda


def serialize_item(item):
    out = {}
    for k, v in item.items():
        try:
            out[k] = json.loads(v)
        except:
            out[k] = v
    return out


def get_dashboards_data(data_dir):
    data = {}
    layout_data = pamda.read_csv(data_dir + "/layout.csv", cast_items=True)
    for item in layout_data:
        id = item.pop("id")
        if id not in data:
            data[id] = {"dashboardLayout": []}
        data[id]["dashboardLayout"].append(serialize_item(item))
    return {"data": data}
