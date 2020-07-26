from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import time


from utilities.general_funcs import *
from utilities.parameters_funcs import * 
from utilities.print_visualize_funcs import *
from utilities.process_csv import *



if __name__ == '__main__':

    # take arguments
    percentage, input_file, target = getArguments(sys.argv)

    # take data and split
    data = readCSVpd(input_file)
    scaler = StandardScaler()
    data_np = scaler.fit_transform(data.values)
    print(data_np)
    data_scaled = pd.DataFrame(data_np, index=data.index, columns=data.columns)


    X, y = getInputTargetDataPd(data_scaled, target)
    # tuned_parameters = [{'kernel': ['linear'], 'C': [0.01, 0.1, 1, 10, 100, 1000]}]

    cut_bins = 5
    y = pd.qcut(y[target], q=cut_bins, labels=False, precision=0)


    hyperparameters = dict(C=[ 0.1, 1, 10, 100])
    linear_svm = LinearSVC(random_state=None, tol=1e-3, max_iter=1000000)
    
    clf = GridSearchCV(linear_svm, hyperparameters, n_jobs=-1, cv=5)
    print("Start fitting GridSearch...")
    start_time = time.time()
    best_model = clf.fit(X, y)
    end_time = time.time()
    print("time:", end_time-start_time)
    print('Best C:', best_model.best_estimator_.get_params()['C'])


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None, shuffle=True)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=None, shuffle=True)

    # standardize data with mean 0
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_val = scaler.transform(X_val)

    linear_svm = LinearSVC(C=best_model.best_estimator_.get_params()['C'], dual=False, tol=1e-3, max_iter=1000000)
    linear_svm.fit(X_train, y_train)
    y_pred_val = linear_svm.predict(X_val)
    print("\npredicting with validation data:\n", classification_report(y_val, y_pred_val))

    y_pred_test = linear_svm.predict(X_test)
    print("\npredicting with test data:\n", classification_report(y_test, y_pred_test))

    kf = KFold(n_splits=5, random_state=None, shuffle=True)
    scores = cross_val_score(linear_svm, X, y, cv=kf, scoring='accuracy')
    print("Accuracy: %0.2f" % (scores.mean()))