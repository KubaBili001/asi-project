"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines():
    from asi_26c_4.pipelines.data_processing import create_pipeline as create_data_processing_pipeline
    from asi_26c_4.pipelines.data_verification import create_pipeline as create_data_verification_pipeline
    from asi_26c_4.pipelines.data_vizualization import create_pipeline as create_data_viz_pipeline
    from asi_26c_4.pipelines.machine_learning import create_pipeline as create_machine_learning_pipeline
    from asi_26c_4.pipelines.model_evaluation import create_pipeline as create_model_evaluation_pipeline
    from asi_26c_4.pipelines.autogluon import create_pipeline as create_autogluon_pipeline

    data_processing_pipeline = create_data_processing_pipeline()
    data_verification_pipeline = create_data_verification_pipeline()
    data_viz_pipeline = create_data_viz_pipeline()
    machine_learning_pipeline = create_machine_learning_pipeline()
    model_evaluation_pipeline = create_model_evaluation_pipeline()
    autogluon_pipeline = create_autogluon_pipeline()

    return {
        "data_processing": data_processing_pipeline,
        "data_verification": data_verification_pipeline,
        "data_vizualization": data_viz_pipeline,
        "machine_learning": machine_learning_pipeline,
        "model_evaluation": model_evaluation_pipeline,
        "autogluon" : autogluon_pipeline,
        "__default__": (
            data_processing_pipeline + data_verification_pipeline +
            data_viz_pipeline + machine_learning_pipeline + model_evaluation_pipeline + autogluon_pipeline
        )
    }
