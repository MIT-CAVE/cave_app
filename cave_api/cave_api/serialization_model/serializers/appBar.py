import json
from cave_api.serialization_model.utils import read_csv, group_list

def serialize_item(item):
    if item.get('color'):
        item['color'] = json.loads(item['color'])
    return item

def get_app_bar_data(data_dir):
    return {"data": {i.pop("id"): serialize_item(i) for i in read_csv(data_dir + "appBar.csv")}}
