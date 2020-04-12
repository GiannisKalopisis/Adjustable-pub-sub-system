import os.path
import sys
import numpy as np
import pandas as pd 
import csv


# returns average of k previous rows as numpy row
def addAverageRow(k, rows):
    
    new_average_row = []
    last_k_rows_np = np.array(rows[-k:])
    rows_transpose = last_k_rows_np.transpose()

    for row in rows_transpose:
        new_average_row.append(round(sum(row)/k, 5))
        
    return np.array(new_average_row)


if __name__ == '__main__':

    k_average = sys.argv[1]
    input_file = sys.argv[2]
    dest_file = sys.argv[3]

    # make from string to int k_average
    try:
        k_average = int(k_average)
    except (TypeError, ValueError):
        print("Couldn't convert {} to int.".format(k_average))
        sys.exit(1)

    print("Reading file '{}'".format(input_file))
    pd_file = pd.read_csv(input_file, sep='\t', header=None)
    input_file_np = pd_file.to_numpy()

    new_file_rows = []
    counter = 0
    previous_counter = 0
    
    # iterate through every line and take average
    for line in input_file_np:
        counter += 1
        new_file_rows.append(line)
        if (counter % k_average) == 0:
            previous_counter = counter
            new_file_rows.append(addAverageRow(k_average, new_file_rows))


    # write to file
    file_exists = os.path.isfile(dest_file) 
    if file_exists:
        os.remove(dest_file)
        print("Removing old '{}'".format(dest_file))
        print("Creating new '{}'".format(dest_file))
    else:
        print("Creating new file '{}'".format(dest_file))

    with open(dest_file, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = '\t')
        writer.writerows(new_file_rows)
        
    print("Done creating file with average value every {} rows!".format(k_average))