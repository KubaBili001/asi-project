from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
def dropColumns(df, column_names):
    for name in column_names:
        df = df.drop([name], axis=1)
    return df

def encodingData(df, column_names):
    label_encoder = LabelEncoder()
    for name in column_names:
        df[name] = label_encoder.fit_transform(df[name])
    return df

def addRatio(df, target_column_name, val_1, val_2):
    df[target_column_name] = ((df[val_1] + df[val_2]) / df[val_2])
    scaler = MinMaxScaler()
    df[target_column_name] = scaler.fit_transform(df[[target_column_name]])
    return df