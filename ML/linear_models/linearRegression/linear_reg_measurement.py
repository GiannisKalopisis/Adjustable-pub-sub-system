from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
import pandas as pd
import numpy as np
import csv

from utilities.general_funcs import *
from utilities.parameters_funcs import * 
from utilities.print_visualize_funcs import *
from utilities.process_csv import *


scoring_dict = {
    "R2": "r2",
    "Explained Variance": "explained_variance",
    "Mean Absolute Error": "neg_mean_absolute_error",
    "Mean Squared Error": "neg_mean_squared_error",
    "Median Absolute Error": "neg_median_absolute_error"
}

scoring_dict_names = {
    "R2": "R2",
    "EV": "Explained Variance",
    "MAE": "Mean Absolute Error",
    "MSE": "Mean Squared Error",
    "MDE": "Median Absolute Error"
}


filesList= ["../../data/1_parameter/Batch_Size.tsv", "../../data/1_parameter/Buffer_Memory.tsv", "../../data/1_parameter/Linger_Ms.tsv", \
            "../../data/1_parameter/Max_Request_Size.tsv", "../../data/1_parameter/Message_Size.tsv", "../../data/2_parameters/Batch_Size+Buffer_Memory.tsv",
            "../../data/2_parameters/Batch_Size+Linger_Ms.tsv", "../../data/2_parameters/Batch_Size+Max_Request_Size.tsv", "../../data/2_parameters/Buffer_Memory+Linger_Ms.tsv", 
            "../../data/2_parameters/Linger_Ms+Max_Request_Size.tsv"]


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 900)
    
    if len(sys.argv) < 2:
        print("You have to give target as argument.")
        sys.exit(1)
    
    target = sys.argv[1]

    # cross validation 
    percentage = 10

    print("%s:" % (target))
    row = []

    for input_file in filesList:

        print("\n%s:" % (input_file))
        data = readCSVpd(input_file)
        X, y = getInputTargetDataPd(data, target)

        regressor = LinearRegression()
        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)
        # first way with ready cross_validation
        print("Cross Validation (sklearn):")
        for score_param in scoring_dict:
            score = cross_val_score(regressor, X, y, scoring=scoring_dict[score_param], cv=kf)
            print("%s:" % (score_param))
            # print(score)
            print("Accuracy: %0.2f (+/- %0.2f)\n" % (score.mean(), score.std() * 2))
            row.append("{:.2f} (+/- {:.2f})".format(score.mean(), score.std() * 2))


        print("-----------------------")

        # second way with my cross_validation
        print("Cross Validation (my code):")
        R2, EV, MAE, MSE, MDE = [], [], [], [], []
        regressor = LinearRegression()
        for train_index, test_index in kf.split(X.values):
            X_train, X_test = X.values[train_index], X.values[test_index]
            y_train, y_test = y.values[train_index], y.values[test_index]
            regressor.fit(X_train, y_train) # test also fit_transform
            R2.append(getR2Metrics(y_test, regressor.predict(X_test)))
            EV.append(getExplainedVarianceMetrics(y_test, regressor.predict(X_test)))
            MAE.append(getMeanAbsoluteErrorMetrics(y_test, regressor.predict(X_test)))
            MSE.append(getMeanSquaredErrorMetrics(y_test, regressor.predict(X_test)))
            MDE.append(getMedianAbsoluteErrorMetrics(y_test, regressor.predict(X_test)))
        for score_list in [R2, EV, MAE, MSE, MDE]:
            print("%s:" % (scoring_dict_names[namestr(score_list, globals())[0]]))
            # print(score)
            print("Accuracy: %0.2f (+/- %0.2f)\n" % (np.mean(score_list), np.std(score_list) * 2))
            row.append("{:.2f} (+/- {:.2f})".format(np.mean(score_list), np.std(score_list) * 2))

        print("-----------------------")

        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)
        regressor = LinearRegression()
        regressor.fit(X_train, y_train) # test also fit_transform
        y_pred = regressor.predict(X_test)
        # actual_pred_values = get_pred_values_dataframe(Y_test, Y_pred)    # print the actual values
        print("No cross validation :")
        # print(get_coefficient_dataframe(regressor, data.columns.tolist(), target))
        print()
        print('R^2:', r2_score(y_test, y_pred))
        row.append(r2_score(y_test, y_pred))
        print('Explained Variance:', explained_variance_score(y_test, y_pred))
        row.append(explained_variance_score(y_test, y_pred))
        print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
        row.append(mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
        row.append(mean_squared_error(y_test, y_pred))
        print('Median Absolute Error:', median_absolute_error(y_test, y_pred))
        row.append(median_absolute_error(y_test, y_pred))
        
    row = np.reshape(row, (150, 1))
    

    print("\n\nWriting to file:\n")

    _file = "measurements.tsv"
    file_exists = os.path.isfile(_file) 
    if file_exists:
        os.remove(_file)
        print("Removing old '{}'".format(_file))
        print("Creating new '{}'".format(_file))
        file_name = open(_file, "w+")
    else:
        print("Creating new file '{}'".format(_file))
        file_name = open(_file, "w+")
    print("Writing to new '{}'".format(file_name.name))
    with open(file_name.name, 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = '\t')
        writer.writerows(row)

    print("Done!")


        






   

   