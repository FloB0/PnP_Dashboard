import sqlite3
from util import *
import streamlit as st
import pyodbc
import mysql.connector
from sqlalchemy import create_engine, MetaData, Table, insert, exc
from util import *

# Initialize connection.
# Uses st.cache_resource to only run once.

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def insert_into_race(names):
    # Establishing the connection
    connection = init_connection()
    cursor = connection.cursor()

    # SQL query string
    insert_query = "INSERT INTO race (name) VALUES (%s)"

    try:
        for name in names:
            cursor.execute(insert_query, (name,))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        connection.close()

def insert_into_race_alchemy(names):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the race table
    race_table = Table('race', metadata, autoload_with=engine)

    # Create a list of dictionaries to represent all the data to insert
    data_to_insert = [{'name': name} for name in names]

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(race_table).values(data_to_insert)

    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)


def insert_into_race_alchemy_logging(names):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the race table
    race_table = Table('race', metadata, autoload_with=engine)

    # Create a list of dictionaries to represent all the data to insert
    data_to_insert = [{'name': name} for name in names]

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(race_table).values(data_to_insert)
    compiled_stmt = stmt.compile(engine)
    sql_str = str(compiled_stmt)
    params = compiled_stmt.params

    print(f"Generated SQL: {sql_str}")
    print(f"Parameters: {params}")

    # Execute the statement and catch any SQLAlchemy exceptions
    with engine.connect() as connection:
        try:
            result = connection.execute(stmt)
            connection.commit()
            print(f"Rows inserted: {result.rowcount}")
        except Exception as e:
            print(f"Error occurred: {e}")


# Names to insert
race_names = ["was commit the prob"]

# Execute the insertion
insert_into_race_alchemy_logging(race_names)