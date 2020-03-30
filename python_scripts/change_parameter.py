import tempfile
import os.path
import sys
from pathlib import Path
import re
import csv


if __name__ == '__main__':

    change_param = sys.argv[1]
    file_to_change = sys.argv[2]

    # find and open file
    file_exists = os.path.isfile(file_to_change) 
    if file_exists:
        file_name = open(file_to_change, "r")
        print("Opened file '{}'".format(file_to_change))
    else:
        print("Couldn't find file '{}'".format(file_to_change))
        sys.exit(1)

    # Splitting at '=' 
    split_list = change_param.split('=')
    if len(split_list) is 2:
        parameter, value = split_list
    else:
        print("I splitted your parameter in {} arguments than 2.".format(len(split_list)))
        sys.exit(2)

    change_done = False
    temp = tempfile.NamedTemporaryFile(mode="r+")

    #overwrite line
    for num, line in enumerate(file_name.readlines(), 1):
        sline=line.strip().split("=")
        if sline[0].startswith(parameter):
            sline[1] = value
            change_done = True
            print("Changed parameter '{}' at line {}".format(parameter, num))
        elif sline[0].startswith('#' + parameter):
            sline[0] = parameter
            sline[1] = value
            change_done = True
            print("Changed parameter '{}' at line {}".format(parameter, num))
        line = '='.join(sline)
        temp.write(line.rstrip()+"\n")
    file_name.close()

    # seek and overwrite file
    temp.seek(0)
    with open(file_to_change, "w") as overwritting_file:
        for line in temp:
            overwritting_file.write(line)    
    temp.close()

    # write line at the end of file
    # because didn't find in file
    if not change_done:
        with open(file_to_change, "a") as file_object:
            print("Couldn't find parameter '{}', so I write it to the end of file.".format(parameter))
            file_object.write('\n#new parameter added from script\n' + change_param + '\n')

    