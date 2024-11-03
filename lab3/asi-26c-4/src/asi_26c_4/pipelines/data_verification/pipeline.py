"""
This is a boilerplate pipeline 'data_verification'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import verifyData


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=verifyData,
            inputs="postProcessed_employees",
            outputs="verified_employees",
            name="verifyData_node"
        )
    ])
