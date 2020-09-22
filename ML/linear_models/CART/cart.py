from sklearn import tree
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

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

CROSS_VAL = True

if __name__ == '__main__':

    # take arguments
    percentage, input_file, target = getArguments(sys.argv)

    # take data and split
    data = readCSVpd(input_file)
    X, y = getInputTargetDataPd(data, target)

    # GridSearch preparation
    depths = np.arange(3,31)
    num_leafs = np.arange(2,31)
    decisionTree = tree.DecisionTreeRegressor()
    pipe = Pipeline(steps=[('decisionTree', decisionTree)])
    parameters = dict(decisionTree__max_depth=depths,
                      decisionTree__min_samples_leaf=num_leafs)

    # getting regressor with optimal parameters from grid search
    DTR_gs = GridSearchCV(pipe, parameters)

    y = np.log(y)

    # take best estimator
    X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)
    DTR_gs.fit(X_train, y_train)
    print('Best max depth:', DTR_gs.best_estimator_.get_params()['decisionTree__max_depth'])
    print('Best min samples leaf:', DTR_gs.best_estimator_.get_params()['decisionTree__min_samples_leaf'])
    print(DTR_gs.best_estimator_.get_params(), "\n\n")
    best_estimator = DTR_gs.best_estimator_

    

    if CROSS_VAL:

        print("Cross validation: \n")
        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)
        for score_param in scoring_dict:
            print("%s:" % (score_param))
            cv_results = cross_val_score(best_estimator, X, y, scoring=scoring_dict[score_param], cv=kf, n_jobs=-1)
            print(cv_results)
            print("Accuracy: %0.2f (+/- %0.2f)\n" % (cv_results.mean(), cv_results.std() * 2))
    
    else:

        print("No cross validation: \n")

        best_estimator.fit(X_train, y_train)
        y_pred = best_estimator.predict(X_test)
        print_metrics(y_test, y_pred)


 