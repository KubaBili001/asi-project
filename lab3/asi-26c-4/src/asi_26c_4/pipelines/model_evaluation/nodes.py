"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.9
"""
from sklearn.metrics import mean_squared_error


def evaluateModel(y_test, x_test, y_pred, model):
    y_test = y_test.to_numpy()
    x_test = x_test.to_numpy()
    y_pred = y_pred.to_numpy()
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2_score = model.score(x_test, y_test)
    print('Root Means Square Error = ', rmse)
    print(f"R² Score: {r2_score}")
    logger.info("Model has a Root Means Square Error on test data", rmse)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", r2_score)


def evaluateCrossValidation(scores):
    scores = scores.to_numpy()
    print("Cross Validation Scores: ", scores)
    print("Average CV Score: ", scores.mean())
    print("Number of CV Scores used in Average: ", len(scores))
