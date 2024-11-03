"""
This is a boilerplate pipeline 'machine_learning'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=prepareSets,
            inputs=["postProcessed_employees_after_satviz", "params:label_to_drop"],
            outputs=["X", "y"],
            name="prepareSets_node"
        ),
        node(
            func=splitData,
            inputs=["X", "y", "params:test_size", "params:train_size", "params:random_state"],
            outputs=["X_train", "X_test", "y_train", "y_test"],
            name="splitSets_node"
        ),
        node(
            func=trainLinearRegression,
            inputs=["X_train", "y_train"],
            outputs="regressor",
            name="trainedLinearRegressionSets_node"
        ),
        node(
            func=crossValidate,
            inputs=["regressor", "X_train", "y_train", "params:n_splits"],
            outputs="Scores_lr",
            name="crossValidatedSets_node_lr"
        ),
        node(
            func=predictLinearRegression,
            inputs=["regressor", "X_test"],
            outputs="y_pred_lr",
            name="predictedLinearRegressionSets_node"
        ),
        node(
            func=trainDecisionTree,
            inputs=["X_train", "y_train", "params:random_state"],
            outputs="decisionTreeRegressor",
            name="trainedDecisionTreeSets_node"
        ),
        node(
            func=crossValidate,
            inputs=["decisionTreeRegressor", "X_train", "y_train", "params:n_splits"],
            outputs="Scores_dt",
            name="crossValidatedSets_node_dt"
        ),
        node(
            func=predictDecisionTree,
            inputs=["decisionTreeRegressor", "X_test"],
            outputs="y_pred_dt",
            name="predictedDecisionTreeSets_node"
        ),
        node(
            func=trainRandomForestRegressor,
            inputs=["X_train", "y_train", "params:n_estimators", "params:random_state"],
            outputs="randomForestRegressor",
            name="trainedRandomForestSets_node"
        ),
        node(
            func=predictRandomForestRegressor,
            inputs=["randomForestRegressor", "X_test"],
            outputs="y_pred_rf",
            name="predictedRandomForestSets_node"
        )
    ])
