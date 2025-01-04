from typing import Union
import joblib
from fastapi import FastAPI
import sqlite3
import pandas as pd
import numpy as np
import boto3
import tarfile
import os

bucket_name = "asi-project"
key = "training-output/sagemaker-scikit-learn-2025-01-04-14-30-00-418/output/model.tar.gz"
local_tar_path = "model.tar.gz"

s3 = boto3.client("s3")

try:
    s3.download_file(bucket_name, key, local_tar_path)
    print(f"Model pobrany i zapisany jako {local_tar_path}")
except Exception as e:
    print(f"Błąd podczas pobierania pliku z S3: {e}")
    raise

extract_path = "./model"
try:
    with tarfile.open(local_tar_path, "r:gz") as tar:
        tar.extractall(path=extract_path)
    print(f"Model rozpakowany w katalogu: {extract_path}")
except Exception as e:
    print(f"Błąd podczas rozpakowywania pliku: {e}")
    raise

joblib_model_path = os.path.join(extract_path, "model.joblib")
if os.path.exists(joblib_model_path):
    print(f"Model znaleziony pod ścieżką: {joblib_model_path}")
else:
    print("Model .joblib nie został znaleziony!")

model = joblib.load(joblib_model_path)
print("Model załadowany i gotowy do użycia!")


app = FastAPI(debug=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post('/employee/predict/{emp_id}')
def predict_employee(emp_id: int):
    conn = sqlite3.connect('C://Users//maksd//OneDrive//Pulpit//asi-project//database//asidatabase.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(employees);")
    schema = cursor.fetchall()
    column_list = [col[1] for col in schema]

    query = f"SELECT * FROM employees WHERE id == {emp_id};"
    cursor.execute(query)
    emp = cursor.fetchall()

    if not emp:
        return {"error": f"No employee found with id {emp_id}"}

    emp_df = pd.DataFrame(emp, columns=column_list)

    numeric_columns = [
        'Department', 'Gender', 'Age', 'Job_Title',
        'Years_At_Company', 'Education_Level', 'Performance_Score',
        'Monthly_Salary', 'Work_Hours_Per_Week', 'Projects_Handled',
        'Overtime_Hours', 'Sick_Days', 'Remote_Work_Frequency',
        'Team_Size', 'Training_Hours', 'Promotions', 'Overtime_Ratio'
    ]
    for col in numeric_columns:
        emp_df[col] = pd.to_numeric(emp_df[col], errors='coerce')

    emp_df['Resigned'] = emp_df['Resigned'].astype(bool)

    prediction_values = emp_df.iloc[0][[
        'Department', 'Gender', 'Age', 'Job_Title',
        'Years_At_Company', 'Education_Level', 'Performance_Score',
        'Monthly_Salary', 'Work_Hours_Per_Week', 'Projects_Handled',
        'Overtime_Hours', 'Sick_Days', 'Remote_Work_Frequency',
        'Team_Size', 'Training_Hours', 'Promotions', 'Resigned', 'Overtime_Ratio'
    ]].values

    prediction_values = np.array(prediction_values, dtype=float)

    prediction = model.predict([prediction_values])

    return {'prediction': prediction.tolist()}