from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score, explained_variance_score
from matplotlib import pyplot as plt
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


