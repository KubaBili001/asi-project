import os
import streamlit as st
import pandas as pd
from kedro.framework.session import KedroSession
from sklearn.preprocessing import LabelEncoder
from kedro.framework.startup import bootstrap_project

project_path = r"C:\Users\maksd\OneDrive\Pulpit\asi-project\lab3\asi-26c-4"
bootstrap_project(project_path)
session = KedroSession.create()
context = session.load_context()

output_data = session.run(pipeline_name="streamlit")
df = output_data["employees_data"]
model = output_data["loaded_model"]

print(df.head())

department_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
job_title_encoder = LabelEncoder()
education_level_encoder = LabelEncoder()
remote_work_frequency_encoder = LabelEncoder()

df['Department'] = department_encoder.fit_transform(df['Department'])
df['Gender'] = gender_encoder.fit_transform(df['Gender'])
df['Job_Title'] = job_title_encoder.fit_transform(df['Job_Title'])
df['Education_Level'] = education_level_encoder.fit_transform(df['Education_Level'])
df['Remote_Work_Frequency'] = remote_work_frequency_encoder.fit_transform(df['Remote_Work_Frequency'])

st.title("Interaktywna aplikacja ML - Streamlit + Kedro")

st.header("1. Wprowadź dane wejściowe do predykcji")

with st.form("input_form"):
    department = st.selectbox("Department", department_encoder.classes_)
    gender = st.selectbox("Gender", gender_encoder.classes_)
    age = st.number_input("Age", min_value=18, max_value=70, value=30)
    job_title = st.selectbox("Job Title", job_title_encoder.classes_)
    years_at_company = st.number_input("Years At Company", min_value=0, max_value=50, value=5)
    education_level = st.selectbox("Education Level", education_level_encoder.classes_)
    performance_score = st.selectbox("Performance Score", [0, 1, 2, 3, 4, 5])
    monthly_salary = st.number_input("Monthly Salary", min_value=0, value=5000)
    work_hours_per_week = st.number_input("Work Hours Per Week", min_value=0, max_value=168, value=40)
    projects_handled = st.number_input("Projects Handled", min_value=0, value=3)
    overtime_hours = st.number_input("Overtime Hours", min_value=0, value=0)
    sick_days = st.number_input("Sick Days", min_value=0, value=2)
    remote_work_frequency = st.selectbox("Remote Work Frequency", [0, 25, 75, 100])
    team_size = st.number_input("Team Size", min_value=1, value=5)
    training_hours = st.number_input("Training Hours", min_value=0, value=10)
    promotions = st.number_input("Promotions", min_value=0, value=0)
    resigned = st.selectbox("Resigned", [0, 1])
    overtime_ratio = st.number_input("Overtime Ratio", min_value=0.0, max_value=1.0, value=0.2)

    submit_button = st.form_submit_button(label="Uruchom predykcję")

if submit_button:
    department_numeric = department_encoder.transform([department])[0]
    gender_numeric = gender_encoder.transform([gender])[0]
    job_title_numeric = job_title_encoder.transform([job_title])[0]
    education_level_numeric = education_level_encoder.transform([education_level])[0]

    input_data = pd.DataFrame({
        'Department': [department_numeric],
        'Gender': [gender_numeric],
        'Age': [age],
        'Job_Title': [job_title_numeric],
        'Years_At_Company': [years_at_company],
        'Education_Level': [education_level_numeric],
        'Performance_Score': [performance_score],
        'Monthly_Salary': [monthly_salary],
        'Work_Hours_Per_Week': [work_hours_per_week],
        'Projects_Handled': [projects_handled],
        'Overtime_Hours': [overtime_hours],
        'Sick_Days': [sick_days],
        'Remote_Work_Frequency': [remote_work_frequency],
        'Team_Size': [team_size],
        'Training_Hours': [training_hours],
        'Promotions': [promotions],
        'Resigned': [resigned],
        'Overtime_Ratio': [overtime_ratio]
    })

    st.write("Dane wejściowe:")
    st.dataframe(input_data)

    try:
        prediction = model.predict(input_data)
        st.header("2. Wynik predykcji")
        st.write(f"Predykcja modelu: {prediction[0]}")
    except Exception as e:
        st.error(f"Błąd podczas wykonywania predykcji: {e}")
