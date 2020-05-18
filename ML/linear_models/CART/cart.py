from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error
import time
import pandas as pd
import numpy as np

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

CROSS_VAL = True

if __name__ == '__main__':

    # take arguments
    percentage, input_file, target = getArguments(sys.argv)

    # take data and split
    data = readCSVpd(input_file)
    X, y = getInputTargetDataPd(data, target)

    # parameters dictionary
    param_dict = {'max_depth': np.arange(3,31),
                  'min_samples_leaf': np.arange(2,11)}

    # getting regressor with optimal parameters from grid search
    print("Starting gridSearch for tuning Decision Tree parameters.")
    start = time.clock()
    decisionTreeRegressor = GridSearchCV(DecisionTreeRegressor(), param_dict)
    end = time.clock()
    print("Elapsed time for GridSearchCV: {}\n".format(end-start))

    if CROSS_VAL:

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

    else:

        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)


        start = time.clock()
        decisionTreeRegressor.fit(X_train, y_train)
        y_pred = decisionTreeRegressor.predict(X_test)
        print("No cross validation:")
        print_metrics(y_test, y_pred)
        print("Elapsed time: {}".format(time.clock()-start))

