from typing import Union
import joblib
from fastapi import FastAPI
import sqlite3

app = FastAPI()
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

    query = f"SELECT * FROM employees WHERE id == {id};"
    cursor.execute(query)
    emp = cursor.fetchall()

    print(emp[0][0])

    column_list = [
        'id',
        'department', 'gender',
        'age', 'job_title',
        'years_at_company', 'education_level',
        'performance_score', 'monthly_salary',
        'work_hours_per_week', 'projects_handled',
        'overtime_hours', 'sick_days',
        'remote_work_frequency', 'team_size',
        'training_hours', 'promotions',
        'resigned', 'overtime_ratio'
    ]

    # Use a map (dictionary) to store column-value pairs
    emp_map = {column: value for column, value in zip(column_list, emp[0])}

    # Iterate through the map and assign values or perform other operations
    for column, value in emp_map.items():
        print(f"{column}: {value}")  # Example: Printing each column and its value

    prediction_values = [
        int(emp_map['department']), int(emp_map['gender']),
        int(emp_map['age']), int(emp_map['job_title']),
        int(emp_map['years_at_company']), int(emp_map['education_level']),
        int(emp_map['performance_score']), float(emp_map['monthly_salary']),
        int(emp_map['work_hours_per_week']), int(emp_map['projects_handled']),
        int(emp_map['overtime_hours']), int(emp_map['sick_days']),
        int(emp_map['remote_work_frequency']), int(emp_map['team_size']),
        int(emp_map['training_hours']), int(emp_map['promotions']),
        emp_map['resigned'],
        float(emp_map['overtime_ratio'])
    ]

    prediction = model.predict([prediction_values])

    return {
        'prediction': prediction
    }
