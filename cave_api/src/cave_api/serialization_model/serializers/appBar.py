from cave_api.serialization_model.utils import read_csv, group_list

def get_app_bar_data(data_dir):
    data = {i.pop('id'):i for i in read_csv(data_dir+'appBar.csv')}
    dash_layout_data = group_list(read_csv(data_dir+'/dashboardLayout.csv'), 'dashboardId')
    for key, value in dash_layout_data.items():
        if data.get(key,False):
            data[key]['dashboardLayout']=value
    return {'data':data}
