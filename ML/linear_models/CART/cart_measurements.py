from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
import time
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
    
    if len(sys.argv) < 2:
        print("You have to give target as argument.")
        sys.exit(1)
    
    target = sys.argv[1]

    # cross validation 
    percentage = 10

    print("%s:" % (target))
    row = []

    # parameters dictionary
    param_dict = {'max_depth': np.arange(3,30),
                    'min_samples_leaf': np.arange(2,30)}

    for input_file in filesList:

        print("\n%s:" % (input_file))
        data = readCSVpd(input_file)
        X, y = getInputTargetDataPd(data, target)

        # getting regressor with optimal parameters from grid search
        print("Starting gridSearch for tuning Decision Tree parameters.")
        start = time.clock()
        decisionTreeRegressor = GridSearchCV(DecisionTreeRegressor(), param_dict)
        end = time.clock()
        print("Elapsed time for GridSearchCV: {}\n".format(end-start))

        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)

        # cross_validation
        print("Cross Validation (sklearn):")
        for score_param in scoring_dict:
            start = time.clock()
            score = cross_val_score(decisionTreeRegressor, X.values, y.values, scoring=scoring_dict[score_param], cv=kf)
            print("%s:" % (score_param))
            # print(score)
            print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))
            print("Elapsed time: {}\n".format(time.clock()-start))
            row.append("{:.2f} (+/- {:.2f})".format(score.mean(), score.std() * 2))


        print("-----------------------")


        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)

        start = time.clock()
        decisionTreeRegressor.fit(X_train, y_train)
        y_pred = decisionTreeRegressor.predict(X_test)
        print("No cross validation:")
        print_metrics(y_test, y_pred)
        print("Elapsed time: {}".format(time.clock()-start))
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


    row = np.reshape(row, (100, 1))
    
    print("\n\nWriting to file:\n")

    _file = "measurements_" + target.replace(' ', '_') + ".tsv"
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


        






   

   