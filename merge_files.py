from itertools import groupby
from operator import itemgetter


def read_name_id(filename):
    output_list = []
    with open(filename, 'r') as reader:
        for line in reader:
            name_id = tuple(line.split())
            if len(name_id) == 2 and name_id[0].isalpha() and name_id[1].isdigit():
                output_list.append(name_id)
    return output_list


def write_fullname_id(filename, list_of_dict):
    with open(filename, 'w') as writer:
        for d in list_of_dict:
            writer.write('{} {} {}\n'.format(d['firstname'], d['lastname'], d['id']))


def get_list_of_dict(keys, list_of_tuples):
     list_of_dict = [dict(zip(keys, values)) for values in list_of_tuples]
     return list_of_dict


def group_list_of_dict(combined_list):
    merged_list = []
    for key, group in groupby(combined_list, lambda item: item['id']):
        merged = merge_list_of_dict(list(group))
        if 'firstname' in merged.keys() and 'lastname' in merged.keys() and 'id' in merged.keys():
            merged_list.append(merged)
    return merged_list


def merge_list_of_dict(list_of_dict):
    output = dict()
    for d in list_of_dict:
        output.update(d)
    return output


def combine_names(firstname_file, lastname_file, output_file):
    firstname_id_list = get_list_of_dict(('firstname', 'id'), read_name_id(firstname_file))

    lastname_id_list = get_list_of_dict(('lastname', 'id'), read_name_id(lastname_file))

    combined_list = sorted(firstname_id_list + lastname_id_list, key=itemgetter('id'))
    grouped_list = group_list_of_dict(combined_list)

    write_fullname_id(output_file, grouped_list)


    
def main():
    combine_names(firstname_file='input_firstname.txt', lastname_file='input_lastname.txt', output_file='output.txt')


if __name__ == "__main__":
    main()