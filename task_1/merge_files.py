from heapq import merge
from itertools import count, islice
from contextlib import ExitStack
import os
import shutil


def merge_sort_by_id(name_id, name_id_sorted, chunk_folder, chunk_size, delete_chunk_folder):
    os.makedirs(chunk_folder, exist_ok=True) 

    chunk_list = []

    with open(name_id, 'r') as input_reader:
        for index in count(start=1):
        
            chunk_sorted = sorted(islice(input_reader, chunk_size), key = lambda line: int(line.split(' ')[1]))
            
            if not chunk_sorted:
                break
            
            chunk_name = '{}/{}.tmp'.format(chunk_folder, index)
            chunk_list.append(chunk_name)
            
            with open(chunk_name, 'w') as chunk_writer:
                chunk_writer.writelines(chunk_sorted)

    with ExitStack() as stack, open(name_id_sorted, 'w') as output_writer:
        chunks = [stack.enter_context(open(chunk)) for chunk in chunk_list]
        output_writer.writelines(merge(*chunks, key = lambda item: int(item.split(' ')[1])))

    if delete_chunk_folder:
        try:
            shutil.rmtree(chunk_folder)
        except:
            pass


def join_sorted_by_id(firstname_id_sorted, lastname_id_sorted, fullname_id_sorted):
    with open(firstname_id_sorted, 'r') as r1, open(lastname_id_sorted, 'r') as r2, open(fullname_id_sorted, 'w') as wr:
        line1 = r1.readline()
        line2 = r2.readline()
        
        while(line1 != '' and line2 != ''):
            firstname, id1 = line1.split(' ')
            lastname, id2 = line2.split(' ')
            if id1 == id2:
                wr.write('{} {} {}'.format(firstname, lastname, id1))
                line1 = r1.readline()
                line2 = r2.readline()
            elif id1 < id2:
                line1 = r1.readline()
            else:
                line2 = r2.readline()
        

def main():
    merge_sort_by_id(name_id='unsorted_files/firstname_id.txt', name_id_sorted='sorted_files/firstname_id.txt', 
    chunk_folder='chunks', chunk_size=2, delete_chunk_folder=True)

    merge_sort_by_id(name_id='unsorted_files/lastname_id.txt', name_id_sorted='sorted_files/lastname_id.txt', 
    chunk_folder='chunks', chunk_size=2, delete_chunk_folder=True)

    join_sorted_by_id(firstname_id_sorted='sorted_files/firstname_id.txt', lastname_id_sorted='sorted_files/lastname_id.txt', 
    fullname_id_sorted='sorted_files/fullname_id.txt')


if __name__ == "__main__":
    main()
