from cave_api.serialization_model.utils import enumerate_dir, read_csv


def get_category_file_data(data_dir, filename, order):
    data = read_csv(data_dir + filename)
    headers = [i for i in data[0].keys() if i != "id"]
    return {
        "name": filename.replace(".csv", ""),
        "data": {i.pop("id"): i for i in data},
        "nestedStructure": {key: {"name": key, "order": i + 1} for i, key in enumerate(headers)},
        "layoutDirection": "horizontal",
        "order": order,
    }


def get_categories_data(data_dir):
    data_list = [
        get_category_file_data(data_dir, filename, order)
        for order, filename in enumerate_dir(data_dir)
    ]
    return {"allow_modification": False, "data": {i["name"]: i for i in data_list}}
