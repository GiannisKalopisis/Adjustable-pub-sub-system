from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
import csv, os


from utilities.general_funcs import *
from utilities.parameters_funcs import * 
from utilities.print_visualize_funcs import *
from utilities.process_csv import *


filesList= ["../../data/1_parameter/Batch_Size.tsv", "../../data/1_parameter/Buffer_Memory.tsv", 
            "../../data/1_parameter/Linger_Ms.tsv", "../../data/1_parameter/Max_Request_Size.tsv", 
            "../../data/1_parameter/Message_Size.tsv", "../../data/2_parameters/Batch_Size+Buffer_Memory.tsv", 
            "../../data/2_parameters/Batch_Size+Linger_Ms.tsv", "../../data/2_parameters/Batch_Size+Max_Request_Size.tsv", 
            "../../data/2_parameters/Buffer_Memory+Linger_Ms.tsv", "../../data/2_parameters/Linger_Ms+Max_Request_Size.tsv"]

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("You have to give target as argument.")
        sys.exit(1)
    target = sys.argv[1]
    
    # metric = 'precision'
    # metric = 'recall'
    # metric = 'f1-score'
    metric = 'accuracy'

    print("%s:" % (target))
    cut_bins = [2, 3, 5, 7, 10]
    row = []

    for input_file in filesList:

        print("\n%s:" % (input_file))
        data = readCSVpd(input_file)
        X, y = getInputTargetDataPd(data, target)

        X, y_data = getInputTargetDataPd(data, target)

        y = np.log10(y)
        y_copy = y.copy()

        for bucket in cut_bins:

            print("Buckets:", bucket)

            y = pd.qcut(y_data[target], q=bucket, labels=False, precision=0)

            n_neighbors = list(range(1,30))
            hyperparameters = dict(n_neighbors=n_neighbors)
            knn = KNeighborsClassifier()

            clf = GridSearchCV(knn, hyperparameters, cv=10)
            best_model = clf.fit(X, y)
            print('Best n_neighbors:', best_model.best_estimator_.get_params()['n_neighbors'])

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None, shuffle=True)
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=None, shuffle=True)

            knn = KNeighborsClassifier(n_neighbors=best_model.best_estimator_.get_params()['n_neighbors'], algorithm='auto', n_jobs=-1)
            knn.fit(X_train, y_train)
            y_pred_val = knn.predict(X_val)
            dict_pred = classification_report(y_val, y_pred_val, output_dict=True)
            # print("\npredicting with validation data:\n", dict_pred['weighted avg'][metric])
            print("\npredicting with validation data:\n", dict_pred['accuracy'])
            row.append([best_model.best_estimator_.get_params()['n_neighbors'], round(dict_pred['accuracy'], 2)])
            # print("\npredicting with validation data:\n", dict_pred['weighted avg']['precision'])

            y_pred_test = knn.predict(X_test)
            dict_test = classification_report(y_test, y_pred_test, output_dict=True)
            #print("\npredicting with test data:\n", dict_test['weighted avg'][metric])
            print("\npredicting with validation data:\n", dict_test['accuracy'])
            row.append([best_model.best_estimator_.get_params()['n_neighbors'], round(dict_test['accuracy'], 2)])
            # print("\npredicting with validation data:\n", dict_pred['weighted avg']['precision'])

            kf = KFold(n_splits=5, random_state=None, shuffle=True)
            scores = cross_val_score(knn, X, y, cv=kf, scoring='accuracy')
            print("\nAccuracy: %0.2f" % (scores.mean()))
            row.append([best_model.best_estimator_.get_params()['n_neighbors'], round(scores.mean(), 2)])
            print("-----------------------------\n")

        print("================================\n")

    row = np.reshape(row, (150, 2))
    
    print("\n\nWriting to file:\n")

    _file = "measurements_log10.tsv"
    target = target.replace("/", "_")
    target = target.replace(" ", "_")
    metric = metric.replace("-", "_")
    _file = target + "_" + metric + "_" + _file

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

