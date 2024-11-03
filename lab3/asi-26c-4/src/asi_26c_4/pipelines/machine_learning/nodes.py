"""
This is a boilerplate pipeline 'machine_learning'
generated using Kedro 0.19.9
"""
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd


def prepareSets(df, label_name):
    y = df[label_name]
    x = df.drop(label_name, axis=1)
    y.head()
    x.head()
    return x, y


def splitData(x, y, train_size, random_state):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=train_size, random_state=random_state)
    y_test = pd.DataFrame(y_test, columns=['y_test_set'])
    x_test = pd.DataFrame(x_test, columns=['x_test_set'])
    return x_train, x_test, y_train, y_test


def trainLinearRegression(x_train, y_train):
    lin_reg = LinearRegression()
    lin_reg.fit(x_train, y_train)
    return lin_reg


def predictLinearRegression(lin_reg, x_test):
    x_test = x_test.to_numpy()[0]
    y_pred = lin_reg.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['prediction'])
    return y_pred


def trainDecisionTree(x_train, y_train, random_state):
    regressor = DecisionTreeRegressor(random_state=random_state)
    regressor.fit(x_train, y_train)
    return regressor

def predictDecisionTree(regressor, x_test):
    x_test = x_test.to_numpy()[0]
    y_pred = regressor.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['prediction'])
    return y_pred


def trainRandomForestRegressor(x_train, y_train, n_estimators, random_state):
    regressor = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    regressor.fit(x_train, y_train)
    return regressor


def predictRandomForestRegressor(rf_reg, x_test):
    x_test = x_test.to_numpy()[0]
    y_pred = rf_reg.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['prediction'])
    return y_pred


def crossValidate(model, x_train, y_train, n_splits):
    x_train = x_train.to_numpy()[0]
    y_train = y_train.to_numpy()[0]
    k_folds = KFold(n_splits=n_splits)

    scores = cross_val_score(model, x_train, y_train, cv=k_folds)
    scores = pd.DataFrame(scores, columns=['scores'])
    return scores