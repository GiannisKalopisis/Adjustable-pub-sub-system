import pandas as pd


def get_pred_values_dataframe(y_test, y_pred):
    return pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})


# get the predicted values of 𝑏₁, 𝑏₂, ... into a dataframe
def get_coefficient_dataframe(regressor, columns, target):
    columns.remove(target)
    return pd.DataFrame(regressor.coef_.flatten(), columns, columns=['Coefficient'])  # or regressor.coef_[0]
