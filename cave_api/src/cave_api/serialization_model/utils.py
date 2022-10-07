import csv, os

def cast_number(string):
    try:
        float_string = float(string)
        return int(float_string) if float_string == int(float_string) else float_string
    except:
        return string


def read_csv(filename):
    with open(filename) as f:
        file_data = csv.reader(f)
        headers = next(file_data)
        return [dict(zip(headers, map(cast_number, i))) for i in file_data]

def enumerate_dir(directory):
    return enumerate(sorted(os.listdir(directory)))
