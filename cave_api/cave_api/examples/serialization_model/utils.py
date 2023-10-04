import os


def enumerate_dir(directory):
    return enumerate(sorted(os.listdir(directory)))


def group_list(lst, key):
    output = {}
    for i in lst:
        key_value = i.pop(key)
        output[key_value] = output.get(key_value, []) + [i]
    return output


def drop_none(data):
    return [{k: v for k, v in i.items() if v is not None} for i in data]
