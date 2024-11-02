"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import dropColumns, encodingData, addRatio


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=dropColumns,
            inputs=["employees", "columnsToDrop"],
            outputs="preprocessed_employees",
            name="dropColumns_node"
        ),
        node(
            func=encodingData,
            inputs=["preprocessed_employees", "columnsToEncode"],
            outputs="processed_employees",
            name="encodingData_node"
        ),
        node(
            func=addRatio,
            inputs=["processed_employees", "params:new_col_name", 'params:Overtime_Hours', 'params:Work_Hours_Per_Week'],
            outputs="postProcessed_employees",
            name="addRatio_node"
        )
    ])
