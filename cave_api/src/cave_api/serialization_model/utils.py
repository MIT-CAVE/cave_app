import csv, os

def cast_properly(input):
    if isinstance(input, str):
        if input =='':
            return None
        if input.lower() in ['true','false']:
            return bool(input)
        try:
            float_input = float(input)
            return int(float_input) if float_input == int(float_input) else float_input
        except:
            pass
    return input

def serializeRow(headers, values):
    values = [cast_properly(i) for i in values]
    return {headers[i]:values[i] for i in range(len(headers)) if values[i]!=None}


def read_csv(filename):
    with open(filename) as f:
        file_data = csv.reader(f)
        headers = next(file_data)
        return [serializeRow(headers, i) for i in file_data]

def enumerate_dir(directory):
    return enumerate(sorted(os.listdir(directory)))

def group_list(lst, key):
    output = {}
    for i in lst:
        key_value = i.pop(key)
        output[key_value]=output.get(key_value,[])+[i]
    return output
