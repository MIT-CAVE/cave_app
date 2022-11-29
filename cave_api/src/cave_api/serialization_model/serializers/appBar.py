import json
from cave_api.serialization_model.utils import read_csv, group_list


def get_app_bar_data(data_dir):
    data = {i.pop("id"): i for i in read_csv(data_dir + "appBar.csv")}

    dash_layout_data, prop_data, layout_data, grids_data = {}, {}, {}, {}
    try: dash_layout_data = group_list(read_csv(data_dir + "/dashboardLayout.csv"), "dashboardId")
    except: pass
    try: prop_data = group_list(read_csv(data_dir + "/props.csv"), "appBarID")
    except: pass
    try: layout_data = group_list(read_csv(data_dir + "/layout.csv"), "appBarID")
    except: pass
    grids_data = group_list(read_csv(data_dir + "/grids.csv"), "appBarID")
    data_data = group_list(read_csv(data_dir + "/data.csv"), "appBarID")

    for i in data:
        for k, v in data[i].items():
            try: data[i][k] = json.loads(v)
            except: continue

    for key, value in prop_data.items():
        if data.get(key, False):
            data[key]["props"] = {}
            for i in value:
                prop_id, prop_dict = i.pop("propID"), {}
                for k, v in i.items():
                    try: prop_dict[k] = json.loads(v)
                    except: prop_dict[k] = v
                data[key]["props"][prop_id] = prop_dict
    
    for key, value in layout_data.items():
        if data.get(key, False):
            data[key]["layout"] = {}
            for i in value:
                for k, v in i.items():
                    data[key]["layout"][k] = v

    for key, value in grids_data.items():
        if data.get(key, False) and data.get(key).get("layout", False):
            data[key]["layout"]["data"] = {}
            for i in value:
                grid_id, grid_dict = i.pop("gridID"), {}
                for k, v in i.items():
                    try: grid_dict[k] = json.loads(v)
                    except: grid_dict[k] = v
                data[key]["layout"]["data"][grid_id] = grid_dict

    for key, value in data_data.items():
        if data.get(key, False):
            data[key]["data"] = {}
            for i in value:
                data_id, data_dict = i.pop("dataID"), {}
                for k, v in i.items():
                    try: data_dict[k] = json.loads(v)
                    except: data_dict[k] = v
                data[key]["data"][data_id] = data_dict

    for key, value in dash_layout_data.items():
        if data.get(key, False):
            try: data[key]["dashboardLayout"] = json.loads(value)
            except: data[key]["dashboardLayout"] = value
    return {"data": data}
