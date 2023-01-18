from cave_api.serialization_model.utils import read_csv, group_list


def get_enabled_types(layers_data):
    output = {}
    for item in layers_data:
        levelType = item.get("type")
        if item.get("enabled") == True:
            output[levelType] = output.get(levelType, {})
            output[levelType][item.get("id")] = True
    return output


def get_legend_groups(layers_data):
    output = {}
    for item in layers_data:
        itemType = f"{item.get('type')}s"
        itemId = item.get("layerId")
        itemValue = item.get("enabled")
        itemGroup = item.get("legendGroup")
        output[itemGroup] = output.get(itemGroup, {"name": itemGroup})
        output[itemGroup][itemType] = output[itemGroup].get(itemType, {})
        output[itemGroup][itemType][itemId] = {
            "value": item.get("value", False),
            "colorBy": item.get("colorBy",''),
            "sizeBy": item.get("sizeBy",''),
        }
    return output

def serialize_map(layers, viewports):
    viewports = {i.pop("viewportId"): i for i in viewports}
    return {
        "defaultViewport": viewports.pop("default", {}),
        "optionalViewports": viewports,
        "legendGroups": get_legend_groups(layers),
    }

def get_maps_data(data_dir):
    layers_data = group_list(read_csv(data_dir + "layers.csv"), "id")
    viewports = group_list(read_csv(data_dir + "viewports.csv"), "id")
    return {
        "data": {
            key:serialize_map(layers_data[key], viewports[key]) for key in layers_data.keys()
        }
    }
