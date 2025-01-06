"""
This is a boilerplate pipeline 'streamlit_pipeline'
generated using Kedro 0.19.9
"""
import pandas as pd
import joblib

def load_full_data(df_or_path):
    if isinstance(df_or_path, str):
        return pd.read_csv(df_or_path)
    elif isinstance(df_or_path, pd.DataFrame):
        return df_or_path
    else:
        raise TypeError("Input must be a file path or a pandas DataFrame")

def load_data(df_or_path):
    if isinstance(df_or_path, str):
        return pd.read_parquet(df_or_path)
    elif isinstance(df_or_path, pd.DataFrame):
        return df_or_path
    else:
        raise TypeError("Input must be a file path or a pandas DataFrame")

def load_model(model_or_path):
    if isinstance(model_or_path, str):
        try:
            model = joblib.load(model_or_path)
            print(f"Model loaded successfully from: {model_or_path}")
            return model
        except Exception as e:
            raise ValueError(f"Failed to load model from path {model_or_path}: {e}")
    else:
        print("Model provided as an object.")
        return model_or_path
