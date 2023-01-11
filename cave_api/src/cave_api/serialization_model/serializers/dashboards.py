import json
from cave_api.serialization_model.utils import read_csv, group_list

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
    layout_data = read_csv(data_dir + "/layout.csv")
    for item in layout_data:
        id = item.pop('id')
        if id not in data:
            data[id]={
                "dashboardLayout": []
            }
        data[id]["dashboardLayout"].append(serialize_item(item))
    return {"data": data}
