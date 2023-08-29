import streamlit as st
import sqlite3 as sql3
import mysql.connector
from sqlalchemy import create_engine, text, MetaData, Table, select, insert, update, delete, inspect
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo
from sqlalchemy.exc import SQLAlchemyError

import time
from streamlit import session_state as ss

DATABASE_URI = f"mysql+mysqlconnector://{st.secrets['AZURE_SQL']['USERNAME']}:{st.secrets['AZURE_SQL']['PASSWORD']}@{st.secrets['AZURE_SQL']['SERVER']}/{st.secrets['AZURE_SQL']['DATABASE']}"


@st.cache_resource
def init_connection_alchemy():
    engine = create_engine(DATABASE_URI)
    return engine


def get_values_alchemy(table_name: object, column_name: object) -> object:
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

    # print(values)
    return values


# inserts a new character to the database
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
    for column in data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table primary_info.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(data)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


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


def get_stat_by_name_alchemy(in_name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    stats_table = Table('stats', metadata, autoload_with=engine)

    # Construct the SELECT statement
    stmt = select(stats_table).where(stats_table.c.name == in_name)

    # Execute the statement and fetch the result
    with engine.connect() as connection:
        result = connection.execute(stmt).fetchone()

    # If a record was found, return it as a dictionary
    if result:
        return result

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


def update_character_alchemy_updated(table_name, character_id, updated_values):
    engine = init_connection_alchemy()
    metadata = MetaData()
    updated_values.pop('id', None)
    # Use inspect to check if table exists
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        print(f"Table {table_name} does not exist.")
        return False

    table = Table(table_name, metadata, autoload_with=engine)

    existing_columns = set(column.name for column in list(table.columns))
    for column_name in updated_values.keys():
        if column_name not in existing_columns:
            print(f"Column {column_name} does not exist in table {table_name}.")
            return False

    try:
        with engine.connect() as connection:
            record = connection.execute(select(table.columns).where(table.c.id == character_id)).fetchone()

            if record:
                # Update existing record
                # Exclude fields you don't want to update
                fields_to_exclude = {'id', 'name', 'race', 'class'}
                update_values = {k: v for k, v in updated_values.items() if k not in fields_to_exclude}

                upd_stmt = update(table).where(table.c.id == character_id).values(update_values)
                connection.execute(upd_stmt)
                connection.commit()
                return True
            else:
                print(f"Record with id {character_id} not found. No update performed.")
                return False

            connection.commit()
            return True
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return False


def update_character_by_name(table_name, character_name, updated_values):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Use inspect to check if table exists
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        print(f"Table {table_name} does not exist.")
        return False

    table = Table(table_name, metadata, autoload_with=engine)

    existing_columns = set(column.name for column in list(table.columns))
    for column_name in updated_values.keys():
        if column_name not in existing_columns:
            print(f"Column {column_name} does not exist in table {table_name}.")
            return False

    try:
        with engine.connect() as connection:
            # Check if a record with the given name exists
            record = connection.execute(select(table.columns).where(table.c.name == character_name)).fetchone()

            if record:
                # Exclude fields you don't want to update
                fields_to_exclude = {'id', 'name', 'race', 'class'}
                update_values = {k: v for k, v in updated_values.items() if k not in fields_to_exclude}

                # Update the record based on the name
                upd_stmt = update(table).where(table.c.name == character_name).values(update_values)
                connection.execute(upd_stmt)
                connection.commit()
                return True
            else:
                print(f"Record with name {character_name} not found. No update performed.")
                return False
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return False


def update_secondary_alchemy(id, by_session_state):
    if not by_session_state:
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
        print(updated_values)
    else:
        nahkampf = st.session_state.character['kk'] * 2 + st.session_state.character['p'] + st.session_state.character[
            'nahkampf']
        fernkampf = st.session_state.character['p'] + st.session_state.character['wa'] + st.session_state.character[
            'mb'] + st.session_state.character['fernkampf']
        parieren = st.session_state.character['kk'] + st.session_state.character['v'] + st.session_state.character[
            'a'] + st.session_state.character['parieren']
        entweichen = st.session_state.character['v'] * 2 + st.session_state.character['g'] + st.session_state.character[
            'entweichen']
        zähigkeit = st.session_state.character['a'] * 2 + st.session_state.character['pb'] + st.session_state.character[
            'zähigkeit']
        ausweichen = st.session_state.character['v'] + st.session_state.character['wa'] + st.session_state.character[
            'g'] + st.session_state.character['ausweichen']
        tarnung = st.session_state.character['pb'] + st.session_state.character['g'] + st.session_state.character[
            'mb'] + st.session_state.character['tarnung']
        fingerfertigkeit = st.session_state.character['p'] + st.session_state.character['mb'] + \
                           st.session_state.character['tv'] + st.session_state.character['fingerfertigkeit']
        schnelligkeit = st.session_state.character['p'] + st.session_state.character['ini'] * 2 + \
                        st.session_state.character['schnelligkeit']
        nachsetzen = st.session_state.character['v'] + st.session_state.character['wk'] + st.session_state.character[
            'ini'] + st.session_state.character['nachsetzen']
        luegen = st.session_state.character['mb'] + st.session_state.character['c'] * 2 + st.session_state.character[
            'luegen']
        etikette = st.session_state.character['ins'] + st.session_state.character['wi'] + st.session_state.character[
            'c'] + st.session_state.character['etikette']
        handeln = st.session_state.character['intel'] * 2 + st.session_state.character['g'] + \
                  st.session_state.character['handeln']
        ueberzeugen = st.session_state.character['wk'] * 2 + st.session_state.character['ins'] + \
                      st.session_state.character['ueberzeugen']
        einschuechtern = st.session_state.character['kk'] + st.session_state.character['a'] + \
                         st.session_state.character['c'] + st.session_state.character['einschuechtern']
        mechanik = st.session_state.character['tv'] * 2 + st.session_state.character['wi'] + st.session_state.character[
            'mechanik']
        aetherkunde = st.session_state.character['mb'] + st.session_state.character['intel'] + \
                      st.session_state.character['wi'] + st.session_state.character['aetherkunde']
        xenos = st.session_state.character['intel'] + st.session_state.character['wi'] * 2 + st.session_state.character[
            'xenos']
        handwerk = st.session_state.character['p'] + st.session_state.character['tv'] * 2 + st.session_state.character[
            'handwerk']
        steuerung = st.session_state.character['pb'] + st.session_state.character['tv'] + st.session_state.character[
            'wi'] + st.session_state.character['steuerung']
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
        print(updated_values)

    # here this will end in a endless loop -> variables need in a new table
    update_character_alchemy('secondary_info', id, updated_values)


def on_submit_click():
    st.session_state.submitted = True


def on_note_submit_click():
    st.session_state.note_submitted = True


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
    del st.session_state['active_char']


def delete_data_alchemy(table_name, name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the table
    table = Table(table_name, metadata, autoload_with=engine)

    # Build the delete statement based on the "name"
    stmt = delete(table).where(table.c.name == name)

    # Execute the statement
    with engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()

    # Optionally, you can check the number of deleted rows:
    print(f"Deleted {result.rowcount} rows.")


def insert_or_increment_character_item(data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # The table name is hard-coded since we are specifically working with the 'Character_Items' table
    table_name = 'character_items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table {table_name}.")
            return

    # Manually constructing the SQL statement
    sql = text(f"""
        INSERT INTO {table_name} (characterID, itemID, quantity)
        VALUES (:characterID, :itemID, 1)
        ON DUPLICATE KEY UPDATE quantity = quantity + 1
    """)

    with engine.connect() as connection:
        connection.execute(sql, data)
        connection.commit()


def get_id(table_name, name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Assuming the table where items are stored is named 'Items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Create the select statement to get the ItemID for a given item name
    stmt = select(table.c.id).where(table.c.name == name)

    with engine.connect() as connection:
        result = connection.execute(stmt).fetchone()
        if result:
            return result[0]
        else:
            print(f"No ItemID found for item name: {name}")
            return None


def get_stat_id(table_name, name):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Assuming the table where items are stored is named 'Items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Create the select statement to get the ItemID for a given item name
    stmt = select(table.c.stat_id).where(table.c.name == name)

    with engine.connect() as connection:
        result = connection.execute(stmt).fetchone()
        if result:
            return result[0]
        else:
            print(f"No ItemID found for item name: {name}")
            return None


def add_item_to_character(character_id, item_name):
    item_id = get_id(table_name='items', name=item_name)

    if not item_id:
        return

    data = {
        "characterID": character_id,
        "itemID": item_id
    }

    # Here you call your previously created function
    insert_or_increment_character_item(data)


def get_stats_for_item(item_id):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the item_stats and stats tables
    item_stats_table = Table('item_stats', metadata, autoload_with=engine)
    stats_table = Table('stats', metadata, autoload_with=engine)

    # Construct the SELECT statement with JOIN
    stmt = (
        select(
            item_stats_table.c.stat_id,
            stats_table.c.name,
            item_stats_table.c.value
        )
        .join(stats_table, item_stats_table.c.stat_id == stats_table.c.stat_id)
        .where(item_stats_table.c.item_id == item_id)
    )

    # Execute the statement
    with engine.connect() as connection:
        result = connection.execute(stmt).fetchall()

    # Convert results into a list of dictionaries for easier processing
    stats_data = [{"stat_id": row[0], "name": row[1], "value": row[2]} for row in result]

    return stats_data


def decrement_or_delete_character_item(data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # The table name is hard-coded since we are specifically working with the 'character_items' table
    table_name = 'character_items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table {table_name}.")
            return

    # Decrement the quantity by 1, and if the quantity becomes zero, delete the row
    with engine.connect() as connection:
        # Decrement Quantity
        sql = text(f"""
            UPDATE {table_name} 
            SET quantity = quantity - 1 
            WHERE characterID = :characterID AND itemID = :itemID;
        """)
        connection.execute(sql, **data)

        # Delete the row if Quantity is 0
        del_stmt = delete(table).where(
            (table.c.characterID == data['characterID']) &
            (table.c.itemID == data['itemID']) &
            (table.c.Quantity == 0)
        )
        connection.execute(del_stmt)
        connection.commit()


def show_image(image_url):
    st.session_state.show_image = image_url
    return


def delete_item_from_character(character_id, item_name):
    item_id = get_id('items', item_name)

    if not item_id:
        return

    data = {
        "characterID": character_id,
        "itemID": item_id
    }

    # Here you call your previously created function
    decrement_or_delete_character_item(data)


def get_items_for_character(characterID):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # We'll specifically target the 'character_items' table
    table_name = 'character_items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Create the select statement to get all itemID and quantity for the specified characterID
    stmt = select(table.c.itemID, table.c.quantity).where(table.c.characterID == characterID)

    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()

        # Check if we have any results
        if results:
            # Convert the results into a dictionary format for easier access
            items_dict = {row[0]: row[1] for row in results}
            return items_dict
        else:
            print(f"No items found for characterID: {characterID}")
            return {}


def get_item_from_id(itemID):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # We'll specifically target the 'character_items' table
    table_name = 'items'
    table = Table(table_name, metadata, autoload_with=engine)

    # Create the select statement to get all itemID and quantity for the specified characterID
    stmt = select(table.c.name, table.c.image_url, table.c.description).where(table.c.id == itemID)

    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()

        # Check if we have any results
        if results:
            # Convert the results into a dictionary format for easier access
            items_dict = results
            return items_dict
        else:
            print(f"No items found for characterID: {itemID}")
            return {}


def get_layout_character_item(character_id):
    items_from_character = get_items_for_character(character_id)
    layout = []
    layout_iterator = 0
    layout_x = 0
    layout_y = 0
    for key in items_from_character:
        print("X: ", layout_x, " Y: ", layout_y)
        quantity_iterator = 0
        while quantity_iterator < items_from_character[key]:
            dashboard_item = dashboard.Item(str(layout_iterator), layout_x, layout_y, 3, 4)
            layout.append(dashboard_item)
            quantity_iterator += 1
            layout_iterator += 1
            if layout_x < 9:
                layout_x += 3
            else:
                layout_y += 4
                layout_x = 0
        # print("print ",key)
    # print(items_from_character)
    return layout


def create_item_elements_for_character_id(characterID):
    layout = get_layout_character_item(characterID)
    print(layout)
    items = get_items_for_character(characterID)
    item_counter = 0
    with elements("Dashboard Items"):
        with dashboard.Grid(layout, draggableHandle=".draggable"):
            for key in items:
                quantity_iterator = 0
                while quantity_iterator < items[key]:
                    print('layout:', layout[item_counter]['i'])
                    item_list = get_item_from_id(key)
                    # print(item_list)
                    with mui.Card(key=str(item_counter), sx={"display": "flex", "flexDirection": "column"}):
                        quantity_iterator += 1
                        item_counter += 1
                        mui.CardHeader(
                            title=item_list[0][0],
                            action=mui.IconButton(mui.icon.DeleteOutline),
                            className="draggable"
                        )
                        mui.CardMedia(
                            component="img",
                            height=400,
                            width=300,
                            image=item_list[0][1],
                            alt=item_list[0][0],
                        )
                        with mui.CardContent(sx={"flex": 1}):
                            mui.Typography(item_list[0][2])


def increment_stat(stat):
    # Get the current value of the specified attribute from st.session_state
    st.session_state.active_char[stat] = st.session_state.active_char[stat] + 1
    return


def decrement_stat(stat):
    # Get the current value of the specified attribute from st.session_state
    st.session_state.active_char[stat] = st.session_state.active_char[stat] - 1
    return


def stat_adaption(input_value):
    output_value = 0

    while input_value > 0:
        if output_value < 10:
            decrement = 1
        elif output_value < 15:
            decrement = 2
        else:
            decrement = 3

        input_value -= decrement
        if input_value >= 0:
            output_value += 1
        else:
            break

    return output_value


def insert_stat_alchemy(stat_data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the stats table
    table = Table('stats', metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in stat_data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table stats.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(stat_data)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


def insert_trait_alchemy(trait_data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the stats table
    table = Table('traits', metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in trait_data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table stats.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(trait_data)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


def insert_stat_item_relation_alchemy(relation_data):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the item_stats table
    table = Table('item_stats', metadata, autoload_with=engine)

    # Check if provided columns exist in the table
    existing_columns = set(column.name for column in list(table.columns))
    for column in relation_data.keys():
        if column not in existing_columns:
            print(f"Column {column} does not exist in table item_stats.")
            return

    # Use SQLAlchemy's insert() to build the insert statement
    stmt = insert(table).values(relation_data)
    # Execute the statement
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()


def update_stat_by_name(original_stat_name, updated_values):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the stats table
    table = Table('stats', metadata, autoload_with=engine)

    # Use SQLAlchemy's update() to build the update statement
    stmt = (
        update(table)
        .where(table.c.name == original_stat_name)
        .values(updated_values)
    )

    # Execute the statement
    with engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()

    return result.rowcount  # This will return the number of updated rows


def upsert_stat_for_item(args):
    item_id = args['item_id']
    stat_id = args['stat_id']
    value = args['value']

    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the item_stats table
    item_stats_table = Table('item_stats', metadata, autoload_with=engine)

    # First, check if the stat already exists for the item
    stmt = (
        select(item_stats_table.c.stat_id)
        .where(
            (item_stats_table.c.item_id == item_id) &
            (item_stats_table.c.stat_id == stat_id)
        )
    )

    with engine.connect() as connection:
        existing_stat = connection.execute(stmt).fetchone()

        if existing_stat:  # If the stat already exists for the item, update the value
            update_stmt = (
                update(item_stats_table)
                .where(
                    (item_stats_table.c.item_id == item_id) &
                    (item_stats_table.c.stat_id == stat_id)
                )
                .values(value=value)
            )
            connection.execute(update_stmt)
        else:  # If the stat does not exist, insert a new row
            insert_stmt = item_stats_table.insert().values(item_id=item_id, stat_id=stat_id, value=value)
            connection.execute(insert_stmt)

        connection.commit()


def delete_item_stat_relation(item_id, stat_id):
    engine = init_connection_alchemy()
    metadata = MetaData()

    # Reflect the item_stats table
    table = Table('item_stats', metadata, autoload_with=engine)

    # Construct the DELETE statement
    stmt = delete(table).where(
        (table.c.item_id == item_id) & (table.c.stat_id == stat_id)
    )

    # Execute the statement
    with engine.connect() as connection:
        result = connection.execute(stmt)
        connection.commit()

    print(f"Deleted {result.rowcount} rows.")



# stat = {
#     'name': 'nahkampf',
#     'description': 'Der Umgang mit Nahkampfwaffen und das Schadenspotential werden über diesen Wert bestimmt.'
# }
# insert_stat_alchemy(stat)

# 'nahkampf': nahkampf,
# 'fernkampf': fernkampf,
# 'parieren': parieren,
# 'entweichen': entweichen,
# 'zähigkeit': zähigkeit,
# 'ausweichen': ausweichen,
# 'tarnung': tarnung,
# 'fingerfertigkeit': fingerfertigkeit,
# 'schnelligkeit': schnelligkeit,
# 'nachsetzen': nachsetzen,
# 'luegen': luegen,
# 'etikette': etikette,
# 'handeln': handeln,
# 'ueberzeugen': ueberzeugen,
# 'einschuechtern': einschuechtern,
# 'mechanik': mechanik,
# 'aetherkunde': aetherkunde,
# 'xenos': xenos,
# 'handwerk': handwerk,
# 'steuerung': steuerung

# print(get_stat_by_name_alchemy('a'))
