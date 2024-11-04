"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.9
"""
from sklearn.metrics import mean_squared_error
import numpy as np
import wandb



def evaluateModel(y_test, x_test, y_pred, model):
    with wandb.init(project="asi_26c", job_type="evaluate", name="LinearRegression_Prediction") as run:
        y_test = y_test.to_numpy()
        x_test = x_test.to_numpy()
        y_pred = y_pred.to_numpy()
        print(y_test.shape)
        print(y_pred.shape)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2_score = model.score(x_test, y_test)
        print('Root Means Square Error = ', rmse)
        print(f"R² Score: {r2_score}")
        print("Model has a Root Means Square Error on test data", rmse)
        print("Model has a coefficient R^2 on test data.", r2_score)
        wandb.log({"Root Means Square Error": rmse})
        wandb.log({"R^2": r2_score})



def evaluateCrossValidation(scores):
    scores = scores.to_numpy()
    print("Cross Validation Scores: ", scores)
    print("Average CV Score: ", scores.mean())
    print("Number of CV Scores used in Average: ", len(scores))
