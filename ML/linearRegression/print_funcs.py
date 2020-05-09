from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
import numpy as np
import pandas as pd


def plotAverageValueX(x):
    plt.figure(figsize=(15,10))
    plt.tight_layout()
    seabornInstance.distplot(x)
    plt.show()


# print some metrics of our model
def print_metrics(y_test, y_pred):
    print('R^2:', r2_score(y_test, y_pred))
    print('Explained Variance:', explained_variance_score(y_test, y_pred))
    print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
    print('Median Absolute Error:', median_absolute_error(y_test, y_pred))


# print score(𝑅²) of model, 1 is absolute fit and lower is worse
def print_score(regressor, x_test, y_test):
    print("Variance score: ", regressor.score(x_test, y_test), "\n")  # the value of 𝑅²


# print the intercept(𝑏₀) of the regressor
def print_intercept(regressor):
    print("intercept: ", regressor.intercept_, "\n")  # the bias 𝑏₀


# print the slope of the regressor
def print_slope(regressor):
    print("slope: ", regressor.coef_, "\n")  # an array containing 𝑏₁, 𝑏₂, ... respectively


# print the predicted values of 𝑏₁, 𝑏₂, ... into a dataframe
# we transform regressor.coef_ to 1d array
# and x_list also
def print_coefficient_dataframe(regressor, x_list):
    print(pd.DataFrame(regressor.coef_.flatten(), x_list, columns=['Coefficient']))  # or regressor.coef_[0]


def print_best_regressor(test_size, file, target, regressor, x_list, x_test, y_test, y_pred, pred_values_df):
    print("\n\n")
    print("================> Best Model <================")
    print()
    print("File: ", file)
    print("Target: ", target)
    print("Size of test data: ", format(test_size, ".2%"))
    print("Variance score (𝑅²): ", format(regressor.score(x_test, y_test), ".2%"))
    print("Intercept (𝑏₀): ", regressor.intercept_[0])
    print("Coefficients of the model (in dataframe): ")
    print_coefficient_dataframe(regressor, x_list)
    print("Mean Absolute Error: ", metrics.mean_absolute_error(y_test, y_pred))
    print("Mean Squared Error: ", metrics.mean_squared_error(y_test, y_pred))
    print("Root Mean Squared Error: ", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    # print("Predicted values: \n", pred_values_df)
