from sklearn.linear_model import LassoLars, LassoLarsCV
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error
import pandas as pd

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

    # cross validation lasso
    if CROSS_VAL:

        # compute alpha parameter and fit model
        lassolarscv = LassoLarsCV(fit_intercept=True, verbose=False, max_iter=100000, normalize=True, precompute='auto', cv=percentage, max_n_alphas=10000)
        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)

        # cross_validation
        print("Cross Validation (sklearn):")
        for score_param in scoring_dict:
            score = cross_val_score(lassolarscv, X.values, y.values.ravel(), scoring=scoring_dict[score_param], cv=kf)
            print("%s:" % (score_param))
            # print(score)
            print("Accuracy: %0.2f (+/- %0.2f)\n" % (score.mean(), score.std() * 2))


    # classic lasso
    else:

        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)

        # compute alpha parameter and fit model
        lassolarscv = LassoLarsCV(fit_intercept=True, verbose=False, max_iter=100000, normalize=True, precompute='auto', cv=percentage, max_n_alphas=10000)
        lassolarscv.fit(X_train, y_train.ravel())
        print("No cross validation:")
        print_metrics(y_test, lassolarscv.predict(X_test))

        # put alpha parameter to lasso model
        # lasso = Lasso(fit_intercept=True, normalize=True, max_iter=100000)
        # lasso.set_params(alpha=lassocv.alpha_)
        # lasso.fit(X_train, y_train.ravel())
        # print("No cross validation:")
        # print_metrics(y_test, lasso.predict(X_test))
