import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score


def get_pred_values_dataframe(y_test, y_pred):
    return pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})


# get the predicted values of 𝑏₁, 𝑏₂, ... into a dataframe
def get_coefficient_dataframe(regressor, columns, target):
    columns.remove(target)
    return pd.DataFrame(regressor.coef_.flatten(), columns, columns=['Coefficient'])  # or regressor.coef_[0]


def getR2Metrics(y_test, y_pred):
    return r2_score(y_test, y_pred)


def getExplainedVarianceMetrics(y_test, y_pred):
    return explained_variance_score(y_test, y_pred)


def getMeanAbsoluteErrorMetrics(y_test, y_pred):
    return mean_absolute_error(y_test, y_pred)


def getMeanSquaredErrorMetrics(y_test, y_pred):
    return mean_squared_error(y_test, y_pred)


def getMedianAbsoluteErrorMetrics(y_test, y_pred):
    return median_absolute_error(y_test, y_pred)


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]
