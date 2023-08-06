import sqlite3
from util import *
import streamlit as st
import pyodbc
import mysql.connector

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["AZURE_SQL"]["SERVER"],
        database=st.secrets["AZURE_SQL"]["DATABASE"],
        user=st.secrets["AZURE_SQL"]["USERNAME"],
        password=st.secrets["AZURE_SQL"]["PASSWORD"]
    )

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


# Names to insert
race_names = ["Klonkrieger", "Cyborg", "Zelot", "Tech-Priest", "Medium", "Zivilist"]

# Execute the insertion
insert_into_race(race_names)