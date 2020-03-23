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
        # example line: 50000000 records sent, 1916957.405206 records/sec (18.28 MB/sec), 23.09 ms avg latency, 1304.00 ms max latency, 0 ms 50th, 7 ms 95th, 876 ms 99th, 1269 ms 99.9th.
        splitted_last_line = re.split(r'[ \(]+', last_line)
        # print(list(enumerate(splitted_last_line)))
        row.append(splitted_last_line[3])
        row.append(splitted_last_line[5])
        row.append(splitted_last_line[7])
        row.append(splitted_last_line[11])
        row.append(splitted_last_line[15])
        row.append(splitted_last_line[18])
        row.append(splitted_last_line[21])
        row.append(splitted_last_line[24])

        row_list.append(row)

    # write it back to .tsv file
    print("Writing to new '{}'".format(file_name.name))
    with open(file_name.name, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = '\t')
        writer.writerows(row_list)

    print("Done!")