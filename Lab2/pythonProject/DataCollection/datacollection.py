import pandas as pd

def gatherData(path):
    df = pd.read_csv(path)
    print(df.shape)
    df.head()
    return df