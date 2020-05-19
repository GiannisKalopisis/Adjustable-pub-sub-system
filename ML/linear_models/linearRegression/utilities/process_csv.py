import pandas as pd
import numpy as np
import math
import sys
import os


#########################################
#   Read and process file with Pandas   #
#########################################

def readCSVpd(file):
    try:
        data = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
    except FileNotFoundError:
        print("Couldn't find the file '{}'".format(file))
    return data


def getAverageValuePd(data, average_row):
    return data.iloc[average_row:data.shape[0]:average_row + 1]


def getInputTargetDataPd(data, target_column):

    # input data
    input_columns = data.columns.tolist()
    input_columns.remove(target_column)
    input_data = data[input_columns]
    
    # target data
    target_column = [target_column]
    target_data = data[target_column]

    return input_data, target_data


########################################
#   Read and process file with NumPy   #
########################################

def read_csv_np(file_path):
    # read and delete last column with comments
    data = np.genfromtxt(file_path, delimiter='\t', skip_header=4)
    data = np.delete(data, (data.shape[1] - 1), axis=1)

    # delete nan rows from end to start because if i delete from start to end
    # i change the row indexing
    delete_elements = [i for i in range(len(data)) if math.isnan(data[i][0])]
    delete_elements.reverse()
    for i in delete_elements:
        data = np.delete(data, i, axis=0)

    return data


def get_average_value_np(data, average_row):
    return_data = []
    for row in range(average_row, len(data), average_row + 1):
        return_data.append(list(data[row]))
    return return_data


def get_header_np(file_path):
    data_header = pd.read_csv(file_path, sep='\t', encoding='utf-8', header=None, nrows=1)
    header = [i for i in data_header.iloc[0]]
    return header


def get_target_and_input_variables_np(data, header, target_column):
    try:
        target_column_id = header.index(target_column)
    except ValueError:
        print("Couldn't find", target_column, " as header at the input data")
        sys.exit(1)

    # get target variables
    target_variables = [column[target_column_id] for column in data]
    print(target_variables)

    # get input variables (data - (target variables))
    input_variables = data
    [row.pop(target_column_id) for row in input_variables]
    print(input_variables)

    return target_variables, input_variables

