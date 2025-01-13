import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import wandb
import sqlite3
from kedro.framework.session import KedroSession
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from kedro.framework.startup import bootstrap_project

wandb.login()
wandb_run = wandb.init(project="employee-prediction", name="streamlit-pipeline-enhanced")

project_path = r"C:\Users\maksd\OneDrive\Pulpit\asi-project\lab3\asi-26c-4"
bootstrap_project(project_path)
session = KedroSession.create()
context = session.load_context()

output_data = session.run(pipeline_name="streamlit")
df = output_data["employees_data"]
model = output_data["loaded_model"]
full_data = output_data["full_data"]

department_encoder = LabelEncoder()
gender_encoder = LabelEncoder()
job_title_encoder = LabelEncoder()
education_level_encoder = LabelEncoder()
remote_work_frequency_encoder = LabelEncoder()

full_data['Department'] = department_encoder.fit_transform(full_data['Department'])
full_data['Gender'] = gender_encoder.fit_transform(full_data['Gender'])
full_data['Job_Title'] = job_title_encoder.fit_transform(full_data['Job_Title'])
full_data['Education_Level'] = education_level_encoder.fit_transform(full_data['Education_Level'])
full_data['Remote_Work_Frequency'] = remote_work_frequency_encoder.fit_transform(full_data['Remote_Work_Frequency'])

st.title("Interaktywna aplikacja ML - Streamlit + Kedro")

tabs = st.tabs(["Predykcja", "Trenuj Model", "Eksploracja danych"])

def add_employee_to_db(employee_data):
    conn = sqlite3.connect('C://Users//maksd//OneDrive//Pulpit//asi-project//database//asidatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(ID) FROM employees")
    max_id = cursor.fetchone()[0]
    if max_id is None:
        max_id = 0
    new_id = max_id + 1

    employee_values = (new_id, *employee_data.values.flatten())
    cursor.execute("""
        INSERT INTO employees (ID, Department, Gender, Age, Job_Title, Years_At_Company, 
                               Education_Level, Performance_Score, Monthly_Salary, Work_Hours_Per_Week,
                               Projects_Handled, Overtime_Hours, Sick_Days, Remote_Work_Frequency, 
                               Team_Size, Training_Hours, Promotions, Resigned, Overtime_Ratio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employee_values)
    conn.commit()
    conn.close()

    st.success(f"Nowy pracownik został dodany do bazy danych z ID: {new_id}")

with tabs[0]:
    st.header("1. Wybierz opcję predykcji")
    prediction_mode = st.radio(
        "Wybierz metodę predykcji:",
        options=["Wprowadź własne dane", "Skorzystaj z danych pracownika (ID)"]
    )

    def visualize_and_log_prediction(input_data, prediction):
        st.header("3. Wizualizacja wyników")

        fig, ax = plt.subplots(figsize=(8, 6))
        categories = list(input_data.columns)
        values = input_data.values.flatten()
        ax.barh(categories, values, color="skyblue")
        ax.set_title(f"Predykcja: {prediction[0]}")
        ax.set_xlabel("Wartości cech")
        st.pyplot(fig)

        wandb.log({"Feature Values": wandb.Image(fig)})
        plt.close(fig)

        for col, val in zip(input_data.columns, values):
            wandb.log({f"Feature: {col}": val})

        wandb.log({"Prediction": prediction[0]})

    if prediction_mode == "Skorzystaj z danych pracownika (ID)":
        st.header("Wprowadź ID pracownika")
        df = df.drop('Employee_Satisfaction_Score', axis=1)
        employee_id = st.number_input(
            "Wprowadź ID pracownika:",
            min_value=0,
            max_value=len(df) - 1,
            value=0
        )
        if st.button("Uruchom predykcję na danych pracownika"):
            employee_data = df.iloc[employee_id]
            st.write("Dane pracownika:")
            st.dataframe(employee_data.to_frame().T)

            prediction = model.predict(employee_data.to_frame().T)
            st.header("2. Wynik predykcji")
            st.write(f"Predykcja modelu: {prediction[0]}")
            visualize_and_log_prediction(employee_data.to_frame().T, prediction)

    elif prediction_mode == "Wprowadź własne dane":
        st.header("Wprowadź dane wejściowe do predykcji")

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

            prediction = model.predict(input_data)
            st.header("2. Wynik predykcji")
            st.write(f"Predykcja modelu: {prediction[0]}")

            visualize_and_log_prediction(input_data, prediction)

            add_employee_to_db(input_data)

with tabs[1]:
    st.header("Trenuj model")

    if st.button("Rozpocznij trening modelu"):
        project_path = r"C:\Users\maksd\OneDrive\Pulpit\asi-project\lab3\asi-26c-4"
        bootstrap_project(project_path)
        session = KedroSession.create()
        context = session.load_context()

        retrain_output = session.run(pipeline_name="machine_learning",node_names=["prepareSets_node", "splitSets_node", "trainedLinearRegressionSets_node"])
        new_model = retrain_output["regressor"]
        X_test = retrain_output["X_test"]
        y_test = retrain_output["y_test"]

        y_pred = new_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        st.write("Model został ponownie przetrenowany.")
        st.write(f"Średni błąd bezwzględny (MAE): {mae:.2f}")
        st.write(f"Pierwiastek średniego błędu kwadratowego (RMSE): {rmse:.2f}")

        wandb.log({"MAE": mae, "RMSE": rmse})

with tabs[2]:
    st.header("Eksploracja danych")

    conn = sqlite3.connect('C://Users//maksd//OneDrive//Pulpit//asi-project//database//asidatabase.db')
    df_explore = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()

    numeric_columns = [
        'Age', 'Years_At_Company', 'Performance_Score', 'Monthly_Salary',
        'Work_Hours_Per_Week', 'Projects_Handled', 'Overtime_Hours',
        'Sick_Days', 'Remote_Work_Frequency', 'Team_Size',
        'Training_Hours', 'Overtime_Ratio'
    ]

    for col in numeric_columns:
        df_explore[col] = pd.to_numeric(df_explore[col], errors='coerce')

    st.subheader("Podstawowe statystyki danych liczbowych")

    numeric_stats = df_explore[numeric_columns].describe().T[['mean', 'min', 'max']].rename(
        columns={'mean': 'Średnia', 'min': 'Minimalna wartość', 'max': 'Maksymalna wartość'}
    )

    st.dataframe(numeric_stats, use_container_width=True)

    st.subheader("Filtrowanie danych")

    filter_col = st.selectbox("Wybierz kolumnę do filtrowania:", df_explore.columns)

    unique_values = df_explore[filter_col].dropna().unique()
    selected_values = st.multiselect(f"Wybierz wartości w kolumnie '{filter_col}':", unique_values,
                                     default=unique_values)

    filtered_data = df_explore[df_explore[filter_col].isin(selected_values)]

    st.write(f"Zawartość danych dla wybranych filtrów ({len(filtered_data)} rekordów):")
    st.dataframe(filtered_data, use_container_width=True)

    st.subheader("Wizualizacja danych liczbowych")

    column_to_visualize = st.selectbox("Wybierz kolumnę liczbową do wizualizacji:", numeric_columns)

    if st.checkbox("Pokaż histogram"):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df_explore[column_to_visualize].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f"Histogram kolumny: {column_to_visualize}")
        ax.set_xlabel(column_to_visualize)
        ax.set_ylabel("Częstość")
        st.pyplot(fig)

    if st.checkbox("Pokaż wykres pudełkowy"):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(df_explore[column_to_visualize].dropna(), patch_artist=True, boxprops=dict(facecolor="skyblue"))
        ax.set_title(f"Wykres pudełkowy: {column_to_visualize}")
        ax.set_ylabel(column_to_visualize)
        st.pyplot(fig)
