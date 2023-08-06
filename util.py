import streamlit as st
import sqlite3 as sql3
from streamlit import session_state as ss

# raw string database path
db_path = r"C:\Users\wasme\Desktop\database\pnp_characters.db"


def get_values(table_name):
    conn = sql3.connect(db_path)
    c = conn.cursor()

    sql = f'SELECT name FROM {table_name}'

    c.execute(sql)
    values = [row[0] for row in c.fetchall()]

    conn.close()

    return values


def insert_into_table(table_name, name):
    conn = sql3.connect(db_path)
    c = conn.cursor()

    sql = f'INSERT INTO {table_name} (name) VALUES (?)'
    c.execute(sql, (name,))

    conn.commit()
    conn.close()


def update_character(table, character_id, updated_values):
    # Connect to the SQLite database
    conn = sql3.connect(db_path)
    c = conn.cursor()

    # Check if record exists
    c.execute(f'SELECT * FROM {table} WHERE id = ?', (character_id,))
    record = c.fetchone()

    if record is None:
        # If record does not exist, insert new record
        columns = ', '.join(['id'] + list(updated_values.keys()))
        placeholders = ', '.join(['?'] * (len(updated_values) + 1))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        c.execute(sql, (character_id,) + tuple(updated_values.values()))
    else:
        # If record exists, update it
        columns = ', '.join(f'{key} = ?' for key in updated_values.keys())
        sql = f'UPDATE {table} SET {columns} WHERE id = ?'
        c.execute(sql, tuple(updated_values.values()) + (character_id,))

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()


# inserts a new character to the database
def insert_character(character):
    # Connect to the SQLite database
    conn = sql3.connect(db_path)
    c = conn.cursor()

    # Prepare the SQL INSERT statement
    columns = ', '.join(character.keys())
    placeholders = ', '.join('?' * len(character))
    sql = f'INSERT INTO primary_info ({columns}) VALUES ({placeholders})'

    # Execute the INSERT statement with the character attributes as the parameters
    c.execute(sql, tuple(character.values()))

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()


# fetch character data by id
def get_character_by_id(id):
    # Connect to the SQLite database
    conn = sql3.connect(db_path)
    c = conn.cursor()

    # Execute a query to fetch the character record with the specified id
    c.execute(f"SELECT * FROM primary_info WHERE id = ?", (id,))

    # Fetch the record
    record = c.fetchone()

    # Close the connection
    conn.close()

    # If a record was found, return it as a dictionary
    if record is not None:
        columns = ['id',
                   'name',
                   'race',
                   'class',
                   'kk',
                   'a',
                   'p',
                   'pb',
                   'v',
                   'int',
                   'wk',
                   'wa',
                   'mb',
                   'ins',
                   'ini',
                   'tv',
                   'g',
                   'wi',
                   'c',
                   'nahkampf',
                   'fernkampf',
                   'parieren',
                   'entweichen',
                   'zähigkeit',
                   'ausweichen',
                   'tarnung',
                   'fingerfertigkeit',
                   'schnelligkeit',
                   'nachsetzen',
                   'luegen',
                   'etikette',
                   'handeln',
                   'ueberzeugen',
                   'einschuechtern',
                   'mechanik',
                   'aetherkunde',
                   'xenos',
                   'handwerk',
                   'steuerung']
        return dict(zip(columns, record))

    # If no record was found, return None
    return None
    # Add more characters as needed


def update_secondary(id):
    character = get_character_by_id(id)
    nahkampf = character['kk'] * 2 + character['p'] + character['nahkampf']
    fernkampf = character['p'] + character['wa'] + character['mb'] + character['fernkampf']
    parieren = character['kk'] + character['v'] + character['a'] + character['parieren']
    entweichen = character['v'] * 2 + character['g'] + character['entweichen']
    zähigkeit = character['a'] * 2 + character['pb'] + character['zähigkeit']
    ausweichen = character['v'] + character['wa'] + character['g'] + character['ausweichen']
    tarnung = character['pb'] + character['g'] + character['mb'] + character['tarnung']
    fingerfertigkeit = character['p'] + character['mb'] + character['tv'] + character['fingerfertigkeit']
    schnelligkeit = character['p'] + character['ini'] * 2 + character['schnelligkeit']
    nachsetzen = character['v'] + character['wk'] + character['ini'] + character['nachsetzen']
    luegen = character['mb'] + character['c'] * 2 + character['luegen']
    etikette = character['ins'] + character['wi'] + character['c'] + character['etikette']
    handeln = character['int'] * 2 + character['g'] + character['handeln']
    ueberzeugen = character['wk'] * 2 + character['ins'] + character['ueberzeugen']
    einschuechtern = character['kk'] + character['a'] + character['c'] + character['einschuechtern']
    mechanik = character['tv'] * 2 + character['wi'] + character['mechanik']
    aetherkunde = character['mb'] + character['int'] + character['wi'] + character['aetherkunde']
    xenos = character['int'] + character['wi'] * 2 + character['xenos']
    handwerk = character['p'] + character['tv'] * 2 + character['handwerk']
    steuerung = character['pb'] + character['tv'] + character['wi'] + character['steuerung']
    updated_values = {
        'nahkampf': nahkampf,
        'fernkampf': fernkampf,
        'parieren': parieren,
        'entweichen': entweichen,
        'zähigkeit': zähigkeit,
        'ausweichen': ausweichen,
        'tarnung': tarnung,
        'fingerfertigkeit': fingerfertigkeit,
        'schnelligkeit': schnelligkeit,
        'nachsetzen': nachsetzen,
        'luegen': luegen,
        'etikette': etikette,
        'handeln': handeln,
        'ueberzeugen': ueberzeugen,
        'einschuechtern': einschuechtern,
        'mechanik': mechanik,
        'aetherkunde': aetherkunde,
        'xenos': xenos,
        'handwerk': handwerk,
        'steuerung': steuerung
    }
    update_character('secondary_info', id, updated_values)

# def update_primary(id):
