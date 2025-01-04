"""
This is a boilerplate pipeline 'aws_training'
generated using Kedro 0.19.9
"""
import boto3
import sagemaker
from sagemaker.sklearn import SKLearn


def train_model_aws(dummy_input):
    role = "arn:aws:iam::794038233644:role/sagemaker-role"
    region = "eu-north-1"

    print("Rozpoczynanie sesji")
    sagemaker_session = sagemaker.Session()

    input_data_path = "s3://asi-project/dataset/verified_employees.pq"
    output_data_path = "s3://asi-project/training-output/"

    script_path = "C://Users//maksd//OneDrive//Pulpit//asi-project//lab3//asi-26c-4//src//asi_26c_4//pipelines//aws_training//train.py"

    sklearn_estimator = SKLearn(
        entry_point=script_path,
        role=role,
        instance_type="ml.m5.xlarge",
        instance_count=1,
        framework_version="1.0-1",
        output_path=output_data_path,
        sagemaker_session=sagemaker_session,
    )

    sklearn_estimator.fit({"train": input_data_path})
    return sklearn_estimator

