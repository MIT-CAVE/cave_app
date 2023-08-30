from cave_api.serialization_model.utils import group_list, drop_none
from pamda import pamda


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
        output[itemGroup][itemType][itemId] = {k:v for k,v in {
            "value": item.get("value", False),
            "colorBy": item.get("colorBy"),
            "sizeBy": item.get("sizeBy"),
        }.items() if v is not None}
    return output


def serialize_map(layers, viewports):
    viewports = {i.pop("viewportId"): i for i in viewports}
    return {
        "defaultViewport": viewports.pop("default", {}),
        "optionalViewports": viewports,
        "legendGroups": get_legend_groups(layers),
    }


def get_maps_data(data_dir):
    layers_data = group_list(drop_none(pamda.read_csv(data_dir + "layers.csv", cast_items=True)), "id")
    viewports = group_list(drop_none(pamda.read_csv(data_dir + "viewports.csv", cast_items=True)), "id")
    return {
        "data": {key: serialize_map(layers_data[key], viewports[key]) for key in layers_data.keys()}
    }