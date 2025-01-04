"""
This is a boilerplate pipeline 'aws_training'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_model_aws,
            inputs="dummy_input",
            outputs="sklearn_estimator",
            name="train_model_aws",
        )
    ])
