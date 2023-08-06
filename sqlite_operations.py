import sqlite3
from util import *

# raw string database path
db_path = r"C:\Users\wasme\Desktop\database\pnp_characters.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS secondary_info (
        id INTEGER,
        nahkampf INTEGER,
        fernkampf INTEGER,
        parieren INTEGER,
        entweichen INTEGER,
        zähigkeit INTEGER,
        ausweichen INTEGER,
        tarnung INTEGER,
        fingerfertigkeit INTEGER,
        schnelligkeit INTEGER,
        nachsetzen INTEGER,
        luegen INTEGER,
        etikette INTEGER,
        handeln INTEGER,
        ueberzeugen INTEGER,
        einschuechtern INTEGER,
        mechanik INTEGER,
        aetherkunde INTEGER,
        xenos INTEGER,
        handwerk INTEGER,
        steuerung INTEGER,
        FOREIGN KEY (id) REFERENCES primary_info (id)
    )
''')


# Save (commit) the changes and close the connection
conn.commit()
conn.close()
