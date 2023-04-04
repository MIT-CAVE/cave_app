import csv, os


def enumerate_dir(directory):
    return enumerate(sorted(os.listdir(directory)))


def group_list(lst, key):
    output = {}
    for i in lst:
        key_value = i.pop(key)
        output[key_value] = output.get(key_value, []) + [i]
    return output
