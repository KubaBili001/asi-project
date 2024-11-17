"""
This is a boilerplate pipeline 'autogluon'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import runautogluon


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=runautogluon,
            inputs=["employees"],
            outputs="results",
            name="autogluon_node"
        )
    ])
