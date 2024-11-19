"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=evaluateModel,
            inputs=["y_test", "X_test", "y_pred_lr", "regressor"],
            outputs=None,
            name="evaluationLinearRegression_node"
        ),
        node(
            func=evaluateCrossValidation,
            inputs=["Scores_lr"],
            outputs=None,
            name="crossValidationEvaluationLinearRegression_node"
        ),
        node(
            func=createLearningCurve,
            inputs=["X_train", "y_train", "regressor"],
            outputs=None,
            name="linearregression_learningcurve_node"
        ),
        node(
            func=evaluateModel,
            inputs=["y_test", "X_test", "y_pred_dt", "decisionTreeRegressor"],
            outputs=None,
            name="evaluationDecisionTree_node"
        ),
        node(
            func=evaluateCrossValidation,
            inputs=["Scores_dt"],
            outputs=None,
            name="crossValidationEvaluationDecisionTree_node"
        ),
        node(
            func=createLearningCurve,
            inputs=["X_train", "y_train", "decisionTreeRegressor"],
            outputs=None,
            name="decisionTreeRegressor_learningcurve_node"
        ),
        node(
            func=evaluateModel,
            inputs=["y_test", "X_test", "y_pred_dt", "randomForestRegressor"],
            outputs=None,
            name="evaluationRandomForest_node"
        )
    ])
