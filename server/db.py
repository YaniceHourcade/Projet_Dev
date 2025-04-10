# fichier : server/db.py

import sqlite3

def init_db():
    with open("database/schema.sql", "r") as f:
        schema = f.read()
    conn = sqlite3.connect("database/matchmaking.db")
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Base de données initialisée !")

if __name__ == "__main__":
    init_db()
