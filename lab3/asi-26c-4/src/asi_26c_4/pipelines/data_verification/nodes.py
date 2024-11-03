"""
This is a boilerplate pipeline 'data_verification'
generated using Kedro 0.19.9
"""


def verifyData(df):
    df.info()
    df.isnull().sum().sort_values(ascending=False) / df.shape[0]
    return df