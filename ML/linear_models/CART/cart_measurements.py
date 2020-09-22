from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
from sklearn import tree
from sklearn.pipeline import Pipeline
import time
import pandas as pd
import numpy as np
import csv

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
    percentage = 5

    print("%s:" % (target))
    row = []

    depths = np.arange(3,31)
    num_leafs = np.arange(2,31)

    for input_file in filesList:

        print("\n%s:" % (input_file))
        data = readCSVpd(input_file)
        X, y = getInputTargetDataPd(data, target)

        y = np.log10(y)

        # GridSearch preparation
        decisionTree = tree.DecisionTreeRegressor()
        pipe = Pipeline(steps=[('decisionTree', decisionTree)])
        parameters = dict(decisionTree__max_depth=depths,
                          decisionTree__min_samples_leaf=num_leafs)

        # getting regressor with optimal parameters from grid search
        DTR_gs = GridSearchCV(pipe, parameters)

        # take best estimator
        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)
        DTR_gs.fit(X_train, y_train)
        print('Best max depth:', DTR_gs.best_estimator_.get_params()['decisionTree__max_depth'])
        print('Best min samples leaf:', DTR_gs.best_estimator_.get_params()['decisionTree__min_samples_leaf'])
        print(DTR_gs.best_estimator_.get_params(), "\n\n")
        best_estimator = DTR_gs.best_estimator_

        print("Cross validation: \n")
        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)
        for score_param in scoring_dict:
            print("%s:" % (score_param))
            cv_results = cross_val_score(best_estimator, X, y, scoring=scoring_dict[score_param], cv=kf, n_jobs=-1)
            print(cv_results)
            print("Accuracy: %0.2f\n" % (cv_results.mean(), cv_results.std() * 2))
            row.append("{:.2f}".format(cv_results.mean(), cv_results.std() * 2))
            # row.append(+/- {:.2f}, )

        print("\nNo cross validation: \n")
        best_estimator.fit(X_train, y_train)
        y_pred = best_estimator.predict(X_test)
        # print_metrics(y_test, y_pred)
        print()
        print('R^2:', r2_score(y_test, y_pred))
        row.append(round(r2_score(y_test, y_pred), 2))
        print('Explained Variance:', explained_variance_score(y_test, y_pred))
        row.append(round(explained_variance_score(y_test, y_pred), 2))
        print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
        row.append(round(mean_absolute_error(y_test, y_pred), 2))
        print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
        row.append(round(mean_squared_error(y_test, y_pred), 2))
        print('Median Absolute Error:', median_absolute_error(y_test, y_pred))
        row.append(round(median_absolute_error(y_test, y_pred), 2))

        print("------------------------")



    row = np.reshape(row, (100, 1))
    
    print("\n\nWriting to file:\n")

    _file = "measurements.tsv"
    target = target.replace("/", "_")
    target = target.replace(" ", "_")
    _file = target + "_" + _file

    file_exists = os.path.isfile(_file) 
    if file_exists:
        os.remove(_file)
        print("Removing old '{}'".format(_file))
        print("Creating new '{}'".format(_file))
        file_name = open(_file, 'w+')
    else:
        print("Creating new file '{}'".format(_file))
        file_name = open(_file, 'w+')
    print("Writing to new '{}'".format(file_name.name))
    with open(file_name.name, 'w+', newline = '') as newfile:
        writer = csv.writer(newfile, delimiter = '\t')
        writer.writerows(row)

    print("Done!")


        






   


