def verifyData(df):
    df.info()
    df.isnull().sum().sort_values(ascending=False) / df.shape[0]