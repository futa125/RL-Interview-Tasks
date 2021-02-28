from heapq import merge
from itertools import count, islice
from contextlib import ExitStack
import os
import shutil


def merge_sort_file(input_file, output_file, tmp_file_folder, tmp_file_size):
    """[Takes a file and splits it into select number of smaller tmp files which are sorted by id.
        After that it uses 'heapq.merge' to merge the files back into original sorted file.]

    Args:
        input_file ([String]): [Path to input file]
        output_file ([String]): [Path to output file]
        tmp_file_folder ([String]): [Path to tmp file folder]
        tmp_file_size ([String]): [Number of lines in each tmp file]
    """    
    tmp_file_list = []

    with open(input_file, 'r') as reader:
        for index in count(start=1):
        
            tmp_file_sorted = sorted(islice(reader, tmp_file_size), key = lambda line: int(line.split(' ')[1]))
            
            if not tmp_file_sorted:
                break
            
            tmp_file_name = '{}/{}.tmp'.format(tmp_file_folder, index)
            tmp_file_list.append(tmp_file_name)
            
            with open(tmp_file_name, 'w') as tmp_writer:
                tmp_writer.writelines(tmp_file_sorted)

    with ExitStack() as stack, open(output_file, 'w') as output_writer:
        tmp_files = [stack.enter_context(open(tmp_file)) for tmp_file in tmp_file_list]
        output_writer.writelines(merge(*tmp_files, key = lambda item: int(item.split(' ')[1])))

    clear_folder(tmp_file_folder)


def merge_files(input_file_1, input_file_2, output_file):
    """[Reads two files in parallel and writes them line by line to a new file. 
        Merges first and last name from each file in lines where id is the same]

    Args:
        input_file_1 ([String]): [Path to first input file]
        input_file_2 ([String]): [Path to second input file]
        output_file ([String]): [Path to output file]
    """    
    with open(input_file_1, 'r') as r1, open(input_file_2, 'r') as r2, open(output_file, 'w') as wr:
        for ln1, ln2 in zip(r1, r2):
            ln1 = ln1.split()
            ln2 = ln2.split()
            wr.write('{} {} {}\n'.format(ln1[0], ln2[0], ln2[1]))


def clear_folder(folder_name):
    """[Clears contents of folder used to store tmp files.]

    Args:
        folder_name ([String]): [Path to tmp file folder]
    """    
    for root, dirs, files in os.walk(folder_name):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def main():
    merge_sort_file(input_file='files/input_firstname.txt', output_file='files/output_firstname.txt', 
                    tmp_file_folder='tmp_files', tmp_file_size=1)
    merge_sort_file(input_file='files/input_lastname.txt', output_file='files/output_lastname.txt', 
                    tmp_file_folder='tmp_files', tmp_file_size=1)
    merge_files(input_file_1='files/output_firstname.txt', input_file_2='files/output_lastname.txt', 
                output_file='files/fullname.txt')


if __name__ == "__main__":
    main()
