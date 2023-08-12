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
class_names = ["Klonkrieger", "Cyborg", "Zelot", "Tech-Priest", "Medium", "Zivilist"]
items_to_add = [
    {
        'id': 2,
        'name': "Improvisierte Keule",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/improvisierte_keule_1_d125xb",
        'description': "Ein dicker und langer Gegenstand, der beträchtlichen Schaden anrichten kann ;)"
    },
    {
        'id': 3,
        'name': "Improvisierte Keule",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/improvisierte_keule_2_b1weab",
        'description': "Trifft man damit einen stark gepanzerten Gegner, macht das ein befriedigendes \"GONG\""
    },
    {
        'id': 4,
        'name': "Ein Beil",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/ein_beil_v448i7",
        'description': "Diese Waffe erscheint mir sehr primitiv für die Zukunft"
    },
    {
        'id': 5,
        'name': "Alien-Häcksler",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/alien_häcksler_l8w0rs",
        'description': "\"Teile und Herrsche\", in diem Fall ist Feinde zerteilen gemeint"
    },
    {
        'id': 6,
        'name': "Mittelmäßiges Schwert",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/mittelmäßiges_schwert_tebfht",
        'description': "Es kann eben nicht nur geile Items geben..."
    },
    {
        'id': 7,
        'name': "Space-Schraubenschlüssel",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/space_schraubenzieher_ysv4le",
        'description': "Theoretisch ist das ja ein SchraubenDREHER, aber gut.. Hauptsache man kann damit töten"
    },
    {
        'id': 8,
        'name': "Rostige Stange",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/rostige_stange_kfwmp9",
        'description': "hehe die kann man wieder glatt polieren und anderweitig benutzen"
    },
    {
        'id': 9,
        'name': "Infanterie-Schwert",
        'image_url': "https://res.cloudinary.com/dlzncrunt/image/upload/f_auto,q_auto/infanterie_schwert_y6fo0g",
        'description': "Wer etwas auf sich hält, der prügelt Feinde mit diesem Schwert kaputt"
    }
]


# Execute the insertion
for dict_item in items_to_add:
    print(type(dict_item))
    insert_data_alchemy('items', dict_item)
