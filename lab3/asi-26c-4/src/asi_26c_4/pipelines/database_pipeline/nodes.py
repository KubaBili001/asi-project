"""
This is a boilerplate pipeline 'database_pipeline'
generated using Kedro 0.19.9
"""

import pandas as pd
import sqlite3
import pyarrow.parquet as pa


def create_database_table(path):
    conn = sqlite3.connect('C://Users//maksd//Desktop//asi-project//database//asidatabase.db')
    cursor = conn.cursor()

    df = pd.read_parquet('C://Users//maksd//Desktop//asi-project//lab3//asi-26c-4//data//02_intermediate//verified_employees.pq')
    df.info()
    df.insert(0, 'id', range(1, len(df) + 1))

    table_name = 'employees'

    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)
    cursor.fetchall()

    columns_with_types = ", ".join(
        [f"{col.replace(' ', '_')} TEXT" for col in df.columns if col != 'id'])

    #create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            {columns_with_types}
        );
    """

    cursor.execute(create_table_query)
    cursor.fetchall()

    cursor.execute('pragma table_info(employees);')
    cursor.fetchall()

    for index, row in df.iterrows():
        values = ", ".join([f'"{row_item}"' for row_item in row])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns.str.replace(' ', '_'))}) VALUES ({values})"
        cursor.execute(insert_sql)

    print(df.shape)
    cursor.execute('SELECT COUNT(*) FROM employees')
    cursor.fetchall()

    conn.commit()
    conn.close()

    return df
