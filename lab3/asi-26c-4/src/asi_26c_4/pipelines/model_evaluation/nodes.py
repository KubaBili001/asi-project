"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.9
"""
from sklearn.metrics import mean_squared_error
import numpy as np
import wandb
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt



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


def createLearningCurve(x_train, y_train, model):
    with wandb.init(project="asi_26c", job_type="evaluate", name="Learning_Curve", reinit=True) as run:
        train_sizes, train_scores, validation_scores = learning_curve(
            model, x_train, y_train, cv=5, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10)
        )
        train_scores_mean = np.mean(train_scores, axis=1)
        validation_scores_mean = np.mean(validation_scores, axis=1)

        plt.figure(figsize=(10, 6))
        plt.plot(train_sizes, train_scores_mean, label="Training Score")
        plt.plot(train_sizes, validation_scores_mean, label="Validation Score")
        plt.fill_between(train_sizes, train_scores_mean - np.std(train_scores, axis=1),
                         train_scores_mean + np.std(train_scores, axis=1), alpha=0.1)
        plt.fill_between(train_sizes, validation_scores_mean - np.std(validation_scores, axis=1),
                         validation_scores_mean + np.std(validation_scores, axis=1), alpha=0.1)

        plt.title(f"Learning Curve: {model}")
        plt.xlabel("Training Set Size")
        plt.ylabel("R² Score")
        plt.legend(loc="best")
        plt.grid()
        wandb.log({"learning_curve": wandb.Image(plt)})
        plt.close()


def evaluateCrossValidation(scores):
    scores = scores.to_numpy()
    print("Cross Validation Scores: ", scores)
    print("Average CV Score: ", scores.mean())
    print("Number of CV Scores used in Average: ", len(scores))
