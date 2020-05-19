from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
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
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 900)

    # take arguments
    percentage, input_file, target = getArguments(sys.argv)

    data = readCSVpd(input_file)
    X, y = getInputTargetDataPd(data, target)

    # cross validation 
    if CROSS_VAL:

        regressor = LinearRegression()
        kf = KFold(n_splits=percentage, random_state=None, shuffle=True)

        # first way with ready cross_validation
        print("Cross Validation (sklearn):")
        for score_param in scoring_dict:
            score = cross_val_score(regressor, X, y, scoring=scoring_dict[score_param], cv=kf)
            print("%s:" % (score_param))
            # print(score)
            print("Accuracy: %0.2f (+/- %0.2f)\n" % (score.mean(), score.std() * 2))

        # second way with my cross_validation
        print("Cross Validation (my code):")
        R2, EV, MAE, MSE, MDE = [], [], [], [], []
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

    # classic linear regression
    else:
        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=(percentage/100), random_state=None, shuffle=True)

        regressor = LinearRegression()
        regressor.fit(X_train, y_train) # test also fit_transform

        y_pred = regressor.predict(X_test)
        # actual_pred_values = get_pred_values_dataframe(Y_test, Y_pred)    # print the actual values
        print("No cross validation :")
        print(get_coefficient_dataframe(regressor, data.columns.tolist(), target))
        print()

        print_metrics(y_test, y_pred)
        






   

   