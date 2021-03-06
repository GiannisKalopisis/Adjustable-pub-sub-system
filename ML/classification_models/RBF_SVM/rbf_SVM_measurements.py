from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import csv, os, time


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
    metric = 'f1-score'


    print("%s:" % (target))
    cut_bins = [2, 3, 5, 7, 10]
    row = []

    for input_file in filesList:

        print("\n%s:" % (input_file))
        data = readCSVpd(input_file)
        scaler = StandardScaler()
        data_np = scaler.fit_transform(data.values)
        print(data_np)
        data_scaled = pd.DataFrame(data_np, index=data.index, columns=data.columns)
        X, y = getInputTargetDataPd(data_scaled, target)

        X, y_data = getInputTargetDataPd(data_scaled, target)
        y_copy = y.copy()

        for bucket in cut_bins:

            print("Buckets:", bucket)

            y = pd.qcut(y_data[target], q=bucket, labels=False, precision=0)

            hyperparameters = dict(C=[ 0.1, 1, 10, 100], gamma=[0.001, 0.01, 0.1, 1, 10, 100])
            rbf_svm = SVC(cache_size=500, random_state=None, tol=1e-3, max_iter=1000000)
            
            # Grid Search
            clf = GridSearchCV(rbf_svm, hyperparameters, n_jobs=-1, cv=5)

            # Counting time for fit
            print("Start fitting GridSearch...")
            start_time = time.time()
            best_model = clf.fit(X, y)
            end_time = time.time()
            print("time:", end_time-start_time)
            print('Best C:', best_model.best_estimator_.get_params()['C'])
            print('Best gamma:', best_model.best_estimator_.get_params()['gamma'])

            # Split data to train, test and validation
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None, shuffle=True)
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=None, shuffle=True)

            rbf_svm = SVC(C=best_model.best_estimator_.get_params()['C'], gamma=best_model.best_estimator_.get_params()['gamma'], cache_size=500, tol=1e-3, max_iter=1000000)
            rbf_svm.fit(X_train, y_train)
            y_pred_val = rbf_svm.predict(X_val)
            dict_pred = classification_report(y_val, y_pred_val, output_dict=True)
            print("\npredicting with validation data:\n", dict_pred['weighted avg'][metric])
            row.append([best_model.best_estimator_.get_params()['C'], best_model.best_estimator_.get_params()['gamma'], dict_pred['weighted avg'][metric]])

            y_pred_test = rbf_svm.predict(X_test)
            dict_test = classification_report(y_test, y_pred_test, output_dict=True)
            print("\npredicting with test data:\n",  dict_test['weighted avg'][metric])
            row.append([best_model.best_estimator_.get_params()['C'], best_model.best_estimator_.get_params()['gamma'],  dict_test['weighted avg'][metric]])

            kf = KFold(n_splits=5, random_state=None, shuffle=True)
            scores = cross_val_score(rbf_svm, X, y, cv=kf, scoring='accuracy')
            print("Accuracy: %0.2f" % (scores.mean()))
            row.append([best_model.best_estimator_.get_params()['C'], best_model.best_estimator_.get_params()['gamma'], scores.mean()])
            print("-----------------------------\n")

        print("================================\n")

    row = np.reshape(row, (150, 3))
    
    print("\n\nWriting to file:\n")


    _file = "measurements.tsv"
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
