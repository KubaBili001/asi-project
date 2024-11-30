from typing import Union
import joblib
from fastapi import FastAPI
import sqlite3
import pandas as pd
import numpy as np


app = FastAPI(debug=True)
joblib_in = open("C://Users//maksd//OneDrive//Pulpit//asi-project//lab3//asi-26c-4//data//06_models//regressor.pkl", "rb")
model=joblib.load(joblib_in)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post('/employee/predict')
def predict_employee(id: int):
    conn = sqlite3.connect('C://Users//maksd//OneDrive//Pulpit//asi-project//database//asidatabase.db')
    cursor = conn.cursor()

    # Get the schema of the employees table
    cursor.execute("PRAGMA table_info(employees);")
    schema = cursor.fetchall()
    column_list = [col[1] for col in schema]

    query = f"SELECT * FROM employees WHERE id == {id};"
    cursor.execute(query)
    emp = cursor.fetchall()

    if not emp:
        return {"error": f"No employee found with id {id}"}

    # Create DataFrame dynamically based on the schema
    emp_df = pd.DataFrame(emp, columns=column_list)

    # Ensure all necessary columns are converted to numeric types
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

    # Perform prediction
    prediction = model.predict([prediction_values])

    return {'prediction': prediction.tolist()}

