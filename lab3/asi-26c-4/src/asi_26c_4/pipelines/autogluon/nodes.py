"""
This is a boilerplate pipeline 'autogluon'
generated using Kedro 0.19.9
"""
from autogluon.tabular import TabularDataset
from autogluon.tabular import TabularPredictor


def runautogluon(df):
    data = TabularDataset(df)
    predictor = TabularPredictor(label='Employee_Satisfaction_Score').fit(df)
    performance = predictor.evaluate(df)
    return performance


