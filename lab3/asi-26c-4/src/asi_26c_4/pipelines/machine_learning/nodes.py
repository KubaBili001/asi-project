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
import wandb


def prepareSets(df, label_name):
    y = df[label_name]
    x = df.drop(label_name, axis=1)
    y.head()
    x.head()
    return x, y


def splitData(x, y,test_size,train_size, random_state):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, train_size=train_size, random_state=random_state)
    print(y_test)
    #y_test = pd.DataFrame(y_test, columns=['y_test_set'])
    y_test = pd.DataFrame(y_test).reset_index(drop=True)
    y_test.columns = ['y_test_set']
    x_test = pd.DataFrame(x_test, columns=['Department',
                                           'Gender',
                                           'Age',
                                           'Job_Title',
                                           'Years_At_Company',
                                           'Education_Level',
                                           'Performance_Score',
                                           'Monthly_Salary',
                                           'Work_Hours_Per_Week',
                                           'Projects_Handled',
                                           'Overtime_Hours',
                                           'Sick_Days',
                                           'Remote_Work_Frequency',
                                           'Team_Size',
                                           'Training_Hours',
                                           'Promotions',
                                           'Resigned',
                                           'Overtime_Ratio'])
    return x_train, x_test, y_train, y_test


def trainLinearRegression(x_train, y_train):
    with wandb.init(project="asi_26c", job_type="train", name="LinearRegression_Training") as run:
        lin_reg = LinearRegression()
        lin_reg.fit(x_train, y_train)
        wandb.config.update({"model": "LinearRegression"}, allow_val_change=True)
        wandb.log({"training_score": lin_reg.score(x_train, y_train)})
    return lin_reg


def predictLinearRegression(lin_reg, x_test):
    with wandb.init(project="asi_26c", job_type="predict", name="LinearRegression_Prediction") as run:
        x_test = x_test.to_numpy()
        print("x_test shape: ", x_test.shape)
        y_pred = lin_reg.predict(x_test)
        y_pred = pd.DataFrame(y_pred, columns=['prediction'])
        wandb.log({"predictions": y_pred.head(5).to_dict()})
        wandb.finish()
    return y_pred


def trainDecisionTree(x_train, y_train, random_state):
    with wandb.init(project="asi_26c", job_type="train", name="DecisionTree_Training") as run:
        regressor = DecisionTreeRegressor(random_state=random_state)
        regressor.fit(x_train, y_train)

        wandb.config.update({"model": "DecisionTree", "random_state": random_state}, allow_val_change=True)
        wandb.log({"training_score": regressor.score(x_train, y_train)})
    return regressor

def predictDecisionTree(regressor, x_test):
    with wandb.init(project="asi_26c", job_type="predict", name="DecisionTree_Prediction") as run:
        #x_test = x_test.to_numpy()
        print("x_test shape: ", x_test.shape)
        y_pred = regressor.predict(x_test)
        y_pred = pd.DataFrame(y_pred, columns=['prediction'])
        wandb.log({"predictions": y_pred.head(5).to_dict()})
        wandb.finish()
    return y_pred


def trainRandomForestRegressor(x_train, y_train, n_estimators, random_state):
    with wandb.init(project="asi_26c", job_type="train", name="RandomForest_Training") as run:
        regressor = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        regressor.fit(x_train, y_train)

        wandb.config.update({"model": "RandomForest", "n_estimators": n_estimators, "random_state": random_state}, allow_val_change=True)
        wandb.log({"training_score": regressor.score(x_train, y_train)})
    return regressor


def predictRandomForestRegressor(rf_reg, x_test):
    with wandb.init(project="asi_26c", job_type="predict", name="RandomForest_Prediction") as run:

        x_test = x_test.to_numpy()
        y_pred = rf_reg.predict(x_test)
        y_pred = pd.DataFrame(y_pred, columns=['prediction'])

        wandb.log({"predictions": y_pred.head(5).to_dict()})
        wandb.finish()
    return y_pred


def crossValidate(model, x_train, y_train, n_splits):
    with wandb.init(project="asi_26c", job_type="cross_validation", name="CrossValidation") as run:
        x_train = x_train.to_numpy()
        y_train = y_train.to_numpy()
        k_folds = KFold(n_splits=n_splits)
        print("x_train shape: ", x_train.shape)
        print("y_train shape: ", y_train.shape)
        #x_train = x_train.reshape(X_train.shape[1:])

        scores = cross_val_score(model, x_train, y_train, cv=k_folds)
        scores = pd.DataFrame(scores, columns=['scores'])
        wandb.log({"cv_results": scores})
        return scores