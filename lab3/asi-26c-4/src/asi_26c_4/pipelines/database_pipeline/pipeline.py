"""
This is a boilerplate pipeline 'database_pipeline'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_database_table,
            inputs=['verified_employees'],
            outputs='employees_database',
            name="database_node"
        )
    ])
