from cave_api.serialization_model.utils import read_csv, group_list

def get_enabled_types(layers_data):
    output={}
    for item in layers_data:
        levelType=item.get('type')
        output[levelType]=output.get(levelType,{})
        output[levelType][item.get('id')]=item.get('enabled')
    return output

def get_legend_groups(layers_data):
    output={}
    for item in layers_data:
        itemType=item.get('type')
        itemGroup=item.get('legendGroup')
        itemId=item.get('id')
        output[itemGroup]=output.get(itemGroup,{'name':itemGroup})
        output[itemGroup][itemType+'Types']=output[itemGroup].get(itemType+'Types',[])+[itemId]
    return list(output.values())

def get_map_data(data_dir):
    layers_data = read_csv(data_dir+'layers.csv')
    viewports=group_list(read_csv(data_dir+'viewports.csv'), 'id')
    return {
        'data':{
            'enabledTypes':get_enabled_types(layers_data),
            'defaultViewport': viewports.get('default',{}),
            'optionalViewports': viewports,
            'legendGroups': get_legend_groups(layers_data)
        }
    }
