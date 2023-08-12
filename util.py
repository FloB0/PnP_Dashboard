import streamlit as st
import sqlite3 as sql3
import mysql.connector
from sqlalchemy import create_engine, text, MetaData, Table, select, insert, update, delete
import time
from streamlit import session_state as ss

DATABASE_URI = f"mysql+mysqlconnector://{st.secrets['AZURE_SQL']['USERNAME']}:{st.secrets['AZURE_SQL']['PASSWORD']}@{st.secrets['AZURE_SQL']['SERVER']}/{st.secrets['AZURE_SQL']['DATABASE']}"


@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["AZURE_SQL"]["SERVER"],
        database=st.secrets["AZURE_SQL"]["DATABASE"],
        user=st.secrets["AZURE_SQL"]["USERNAME"],
        password=st.secrets["AZURE_SQL"]["PASSWORD"]
    )


def init_connection_alchemy():
    engine = create_engine(DATABASE_URI)
    return engine


def get_values(table_name):
    conn = init_connection()
    c = conn.connect()

    sql = f'SELECT name FROM {table_name}'

    c.execute(sql)
    values = [row[0] for row in c.fetchall()]

    conn.close()

    return values


def get_values_alchemy(table_name, column_name):
    engine = init_connection_alchemy()

    # Your database name
    db_name = st.secrets["AZURE_SQL"]["DATABASE"]  # replace with your actual database name

    # Fetch valid table names from the database
    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{db_name}'"))
        valid_tables = [row[0] for row in result.fetchall()]

    # Validate table name
    if table_name not in valid_tables:
        raise ValueError("Invalid table name")

    # Fetch valid column names for the specified table from the database
    with engine.connect() as connection:
        result = connection.execute(text(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{db_name}'"))
        valid_columns = [row[0] for row in result.fetchall()]

    # Validate column name
    if column_name not in valid_columns:
        raise ValueError("Invalid column name")

    # SQL command to select specified column from the specified table
    sql = text(f"SELECT {column_name} FROM {table_name}")

    with engine.connect() as connection:
        result = connection.execute(sql)
        values = [row[0] for row in result.fetchall()]

    print(values)
    return values


def insert_into_table(table_name, name):
    """
    Inserts into a table, and checks if the table is valid
    table_name: name of a table in the database
    name: value to add as name
    """
    conn = init_connection()
    c = conn.cursor()

    # Check if table exists in the database
    c.execute('SHOW TABLES LIKE %s', (table_name,))
    result = c.fetchone()
    if result is None:
        print(f"Table {table_name} does not exist.")
        return

    sql = f'INSERT INTO {table_name} (name) VALUES (%s)'
    c.execute(sql, (name,))

    conn.commit()
    conn.close()


def insert_into_table_alchemy(table_name, name):
    """
    Inserts into a table, and checks if the table is valid
    table_name: name of a table in the database
    name: value to add as name
    """
    engine = init_connection_alchemy()
    metadata = MetaData()

    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, table_name):
            print(f"Table {table_name} does not exist.")
            return

        # Assuming column name 'name' exists in your table.
        table = Table(table_name, metadata, autoload_with=engine)
        insert_stmt = table.insert().values(name=name)

        connection.execute(insert_stmt)
        connection.commit()


def update_character(table, character_id, updated_values):
    # Connect to the MySQL database
    conn = init_connection()
    c = conn.cursor()

    # Check if table exists in the database
    c.execute('SHOW TABLES LIKE %s', (table,))
    result = c.fetchone()
    if result is None:
        print(f"Table {table} does not exist.")
        return

    # Check if provided columns exist in the table
    c.execute(f'SHOW COLUMNS FROM {table}')
    existing_columns = [column[0] for column in c.fetchall()]
    for column in updated_values.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table {table}.")
            return

    # Check if record exists
    c.execute(f'SELECT * FROM {table} WHERE id = %s', (character_id,))
    record = c.fetchone()

    if record is None:
        # If record does not exist, insert new record
        columns = ', '.join(['id'] + list(updated_values.keys()))
        placeholders = ', '.join(['%s'] * (len(updated_values) + 1))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        c.execute(sql, (character_id,) + tuple(updated_values.values()))
    else:
        # If record exists, update it
        columns = ', '.join(f'{key} = %s' for key in updated_values.keys())
        sql = f'UPDATE {table} SET {columns} WHERE id = %s'
        c.execute(sql, tuple(updated_values.values()) + (character_id,))

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()


def update_character_alchemy(table_name, character_id, updated_values):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Check if table exists in the database
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, table_name):
            print(f"Table {table_name} does not exist.")
            return

        # Autoload the table structure
        table = Table(table_name, metadata, autoload_with=engine)

        # Check if provided columns exist in the table
        existing_columns = set(column.name for column in list(table.columns))
        for column_name in updated_values.keys():
            if column_name not in existing_columns:
                print(f"Column {column_name} does not exist in table {table_name}.")
                return

        # Check if record exists
        record = connection.execute(select([table]).where(table.c.id.eq(character_id))).fetchone()

        if record is None:
            # If record does not exist, insert new record
            ins_stmt = insert(table).values(id=character_id, **updated_values)
            connection.execute(ins_stmt)
        else:
            # If record exists, update it
            upd_stmt = update(table).where(table.c.id.eq(character_id)).values(updated_values)
            connection.execute(upd_stmt)


# inserts a new character to the database
def insert_character(character):
    # Connect to the MySQL database
    conn = init_connection()
    c = conn.cursor()

    # Check if table exists in the database
    table = "primary_info"
    c.execute('SHOW TABLES LIKE %s', (table,))
    result = c.fetchone()
    if result is None:
        print(f"Table {table} does not exist.")
        return

    # Check if provided columns exist in the table
    c.execute(f'SHOW COLUMNS FROM {table}')
    existing_columns = [column[0] for column in c.fetchall()]
    for column in character.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table {table}.")
            return

    # Prepare the SQL INSERT statement
    columns = ', '.join(character.keys())
    placeholders = ', '.join(['%s'] * len(character))
    sql = f'INSERT INTO primary_info ({columns}) VALUES ({placeholders})'

    # Execute the INSERT statement with the character attributes as the parameters
    c.execute(sql, tuple(character.values()))

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()


def insert_character_alchemy(character):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table('primary_info', metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in character.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table primary_info.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(character)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


def insert_data_alchemy(table_name, data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table(table_name, metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in table_name.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table primary_info.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(data)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


def get_character_by_id(in_id):
    # Connect to the MySQL database
    conn = init_connection()
    c = conn.cursor()

    # Execute a query to fetch the character record with the specified id
    c.execute(f"SELECT * FROM primary_info WHERE id = %s", (in_id,))

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
                   'intel',
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


def get_character_by_id_alchemy(in_id):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table('primary_info', metadata, autoload_with=engine)

    # Construct the SELECT statement
    stmt = select(table).where(table.c.id == in_id)

    # Execute the statement and fetch the result
    with engine.connect() as connection:
        result = connection.execute(stmt).fetchone()

    # If a record was found, return it as a dictionary
    if result is not None:
        return {result._fields[i]: result[i] for i in range(len(result._fields))}

        # If no record was found, return None
    return None


def get_character_by_name_alchemy(in_name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table('primary_info', metadata, autoload_with=engine)

    # Construct the SELECT statement
    stmt = select(table).where(table.c.name == in_name)

    # Execute the statement and fetch the result
    with engine.connect() as connection:
        result = connection.execute(stmt).fetchone()

    # If a record was found, return it as a dictionary
    if result is not None:
        return {result._fields[i]: result[i] for i in range(len(result._fields))}

        # If no record was found, return None
    return None


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
    handeln = character['intel'] * 2 + character['g'] + character['handeln']
    ueberzeugen = character['wk'] * 2 + character['ins'] + character['ueberzeugen']
    einschuechtern = character['kk'] + character['a'] + character['c'] + character['einschuechtern']
    mechanik = character['tv'] * 2 + character['wi'] + character['mechanik']
    aetherkunde = character['mb'] + character['intel'] + character['wi'] + character['aetherkunde']
    xenos = character['intel'] + character['wi'] * 2 + character['xenos']
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


def update_secondary_alchemy(id):
    character = get_character_by_id_alchemy(id)
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
    handeln = character['intel'] * 2 + character['g'] + character['handeln']
    ueberzeugen = character['wk'] * 2 + character['ins'] + character['ueberzeugen']
    einschuechtern = character['kk'] + character['a'] + character['c'] + character['einschuechtern']
    mechanik = character['tv'] * 2 + character['wi'] + character['mechanik']
    aetherkunde = character['mb'] + character['intel'] + character['wi'] + character['aetherkunde']
    xenos = character['intel'] + character['wi'] * 2 + character['xenos']
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
    update_character_alchemy('secondary_info', id, updated_values)


# def update_primary(id):
def show_character_submit_form():

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    with st.form(key='character_form'):
        # fetch dropdown data
        races = get_values_alchemy('race', 'name')
        # classes = get_values_alchemy('class')

        st.write('Character Details')
        name = st.text_input('Name')
        race = st.selectbox('Rasse', races)
        # class_ = st.selectbox('Klasse', classes)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.write('Pysis')
            kk = st.number_input('Körperkraft', value=0, step=1)
            a = st.number_input('Ausdauer', value=0, step=1)
            p = st.number_input('Präzision', value=0, step=1)
            pb = st.number_input('Physische Belastbarkeit', value=0, step=1)
            v = st.number_input('Verhindern', value=0, step=1)
        with c2:
            st.write('Psyche')
            intel = st.number_input('Intelligenz', value=0, step=1)
            wk = st.number_input('Willenskraft', value=0, step=1)
            wa = st.number_input('Wahrnehmung', value=0, step=1)
            mb = st.number_input('Mentale Belastbarkeit', value=0, step=1)
            ins = st.number_input('Inspiration', value=0, step=1)
        with c3:
            st.write('Talente')
            ini = st.number_input('Initiative', value=0, step=1)
            tv = st.number_input('Technisches Verständnis', value=0, step=1)
            g = st.number_input('Glück', value=0, step=1)
            wi = st.number_input('Wissen', value=0, step=1)
            c = st.number_input('Charisma', value=0, step=1)

        # Create the submit button
        submitted = st.form_submit_button("Submit", on_click=on_submit_click)

        # If the submit button is clicked, insert the new character into the SQLite database
        if st.session_state.get('submitted', False):
            print("checkpoint7")
            if name == '':
                print("checkpoint8")
                st.warning('Please enter a name before submitting.')
            elif name in get_values_alchemy('primary_info', 'name'):
                print("checkpoint9")
                st.warning('Name already taken. Please try something else')
            else:
                print("checkpoint10")
                character = {
                    'name': name,
                    'race': race,
                    # 'class': class_,
                    'kk': kk,
                    'a': a,
                    'p': p,
                    'pb': pb,
                    'v': v,
                    'intel': intel,
                    'wk': wk,
                    'wa': wa,
                    'mb': mb,
                    'ins': ins,
                    'ini': ini,
                    'tv': tv,
                    'g': g,
                    'wi': wi,
                    'c': c
                }
                insert_character_alchemy(character)
                st.success('Character created successfully!')
                print("checkpoint11")
                st.session_state.submitted = False
                return


def on_submit_click():
    st.session_state.submitted = True


def delete_character_alchemy(name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table('primary_info', metadata, autoload_with=engine)

    # Build the delete statement based on the "name"
    stmt = delete(table).where(table.c.name == name)

    # Execute the statement
    with engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()

    # Optionally, you can check the number of deleted rows:
    print(f"Deleted {result.rowcount} rows.")
