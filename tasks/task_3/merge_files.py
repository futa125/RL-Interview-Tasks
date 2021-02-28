from itertools import groupby


def read_list_of_dict(filename, keys):
    output_list = []
    
    with open(filename, 'r') as reader:
        for line in reader:
            values = line.split()
            if len(values) == len(keys):
                tmp_dict = dict()
                for key, value in zip(keys, values):
                    tmp_dict[key] = value
            output_list.append(tmp_dict)

    return output_list


def write_list_of_dict(filename, list_of_dict, keys):
    with open(filename, 'w') as writer:
        newline = ''
        for _dict in list_of_dict:
            if set(keys).issubset(_dict.keys()):
                space = ''
                writer.write(newline)
                for key in keys:
                    writer.write('{}{}'.format(space, _dict[key]))
                    space = ' '
                newline = '\n'


def combine_list_of_dict(*lists):
    combined = []
    for _list in lists:
        combined += _list
    return combined


def sort_list_of_dict(*lists, grouping_key, key_type):
    try:
        if key_type == 'num':
            _sorted = sorted(combine_list_of_dict(*lists), key = lambda item: float(item[grouping_key]))
        elif key_type == 'str':
            _sorted = sorted(combine_list_of_dict(*lists), key = lambda item: item[grouping_key])
        else:
            raise Exception("Invalid key type.")
    except (KeyError, ValueError) as _exc:
        _sorted = []
    return _sorted


def group_list_of_dict(*lists, grouping_key, key_type):
    _sorted = sort_list_of_dict(*lists, grouping_key=grouping_key, key_type=key_type)
    grouped = []
    for _k, g in groupby(_sorted, lambda item: item[grouping_key]):
        grouped.append(list(g))
    return grouped


def merge_list_of_dict(*lists, merging_key, key_type):
    grouped = group_list_of_dict(*lists, grouping_key=merging_key, key_type=key_type)
    merged = []
    for group in grouped:
        super_dict = dict()
        for _dict in group:
            super_dict.update(_dict)
        merged.append(super_dict)
    return merged


def main():
    firstname_id = read_list_of_dict(filename='files/input_firstname.txt', keys=['firstname', 'id'])
    lastname_id = read_list_of_dict(filename='files/input_lastname.txt', keys=['lastname', 'id'])
    fullname_id = merge_list_of_dict(firstname_id, lastname_id, merging_key='id', key_type='num')
    write_list_of_dict(filename='files/output_fullname.txt', list_of_dict=fullname_id, keys=['firstname', 'lastname', 'id'])


if __name__ == "__main__":
    main()
