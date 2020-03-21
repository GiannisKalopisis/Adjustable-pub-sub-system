import os.path
import sys
from pathlib import Path
import re
import csv


if __name__ == '__main__':

    directory = sys.argv[1]
    _file = sys.argv[2]

    # delete old file if exists and get the new
    file_exists = os.path.isfile(_file) 
    if file_exists:
        os.remove(_file)
        print("Removing old '{}'".format(_file))
        print("Creating new '{}'".format(_file))
        file_name = open(_file, "w+")
    else:
        print("Creating new file '{}'".format(_file))
        file_name = open(_file, "w+")

    # get list with files in directory
    file_list = []
    entries = Path(directory)
    for entry in entries.iterdir():
        file_list.append(entry.name)

    # read every file
    row_list = []
    for entry in file_list:
        row = []

        # get parameters from the name of the file
        file_params = re.split(r'[_.]+', entry)
        for param in file_params[1:]:
            row.append(param)

        # get last line of file
        with open(directory+entry, 'r') as file:
            last_line = list(file)[-1]
        
        # split last line of file
        # need changes to get the correct arguments from last line
        # now is just checking
        splitted_last_line = re.split(r'[ ]+', last_line)
        row.append(splitted_last_line[1])
        row.append(splitted_last_line[6])
        row.append(splitted_last_line[8])

        row_list.append(row)

    # write it back to .tsv file
    print("Writing to new '{}'".format(file_name.name))
    with open(file_name.name, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = '\t')
        writer.writerows(row_list)

    print("Done!")