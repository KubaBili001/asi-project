"""
This is a boilerplate pipeline 'streamlit_pipeline'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=load_full_data,
            inputs='employees',
            outputs='full_data',
            name='load_full_data',
        ),
        node(
            func=load_data,
            inputs="verified_employees",
            outputs="employees_data",
            name="load_data"
        ),
        node(
            func=load_model,
            inputs="regressor",
            outputs="loaded_model",
            name="load_model"
        )
    ])
