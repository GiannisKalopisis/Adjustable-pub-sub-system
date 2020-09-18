from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score


from utilities.general_funcs import *
from utilities.parameters_funcs import * 
from utilities.print_visualize_funcs import *
from utilities.process_csv import *



CROSS_VAL = False

if __name__ == '__main__':

    # take arguments
    percentage, input_file, target = getArguments(sys.argv)

    # take data and split
    data = readCSVpd(input_file)
    X, y = getInputTargetDataPd(data, target)
    y_copy = y.copy()

    cut_bins = 5

    # 5 numbers from 1 to 5
    # cut_labels = np.linspace(1, cut_bins, num=cut_bins, dtype=int)
    # y = pd.cut(y[target], bins=cut_bins, labels=cut_labels)
    y = pd.qcut(y[target], q=cut_bins, labels=False, precision=0)
    # print(y.value_counts())

    n_neighbors = list(range(1,30))
    hyperparameters = dict(n_neighbors=n_neighbors)
    knn = KNeighborsClassifier()

    clf = GridSearchCV(knn, hyperparameters, cv=10)
    best_model = clf.fit(X, y)
    print('Best n_neighbors:', best_model.best_estimator_.get_params()['n_neighbors'])

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None, shuffle=True)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=None, shuffle=True)
    knn = KNeighborsClassifier(n_neighbors=best_model.best_estimator_.get_params()['n_neighbors'], algorithm='auto', n_jobs=-1)
    knn.fit(x_train, y_train)
    y_pred_val = knn.predict(x_val)
    dict_pred = classification_report(y_val, y_pred_val, output_dict=True)
    print("\npredicting with validation data:\n", dict_pred['weighted avg']['precision'])
    # print("\npredicting with validation data:\n", classification_report(y_val, y_pred_val, output_dict=True))

    y_pred_test = knn.predict(x_test)
    print("\npredicting with test data:\n", classification_report(y_test, y_pred_test))

    kf = KFold(n_splits=5, random_state=None, shuffle=True)
    scores = cross_val_score(knn, X, y, cv=kf, scoring='accuracy')
    print("Accuracy: %0.2f" % (scores.mean()))







   

   
