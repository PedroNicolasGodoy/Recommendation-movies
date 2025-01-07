import sqlite3
import pandas as pd

DATABASE_PATH = "C:/Users/Pedro/Desktop/M-Pindividual/data/database.db"

# Función para leer datos de una tabla SQLite
def query_db(query):
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
