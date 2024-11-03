"""
This is a boilerplate pipeline 'data_vizualization'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import corelation_matrix_vizualization, satisfaction_score_distribution


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=corelation_matrix_vizualization,
            inputs="postProcessed_employees",
            outputs="postProcessed_employees_after_corviz",
            name="corelation_matrix_vizualization_node"
        ),
        node(
            func=satisfaction_score_distribution,
            inputs="postProcessed_employees",
            outputs="postProcessed_employees_after_satviz",
            name="satisfaction_score_distribution_node"
        )
    ])
