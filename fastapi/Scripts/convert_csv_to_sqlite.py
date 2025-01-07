import sqlite3
import pandas as pd

# Rutas de los archivos CSV
MOVIES_CSV = "C:/Users/Pedro/Desktop/M-Pindividual/data/movies.csv"
DIRECTORS_CSV = "C:/Users/Pedro/Desktop/M-Pindividual/data/directors.csv"
CHARACTERS_CSV = "C:/Users/Pedro/Desktop/M-Pindividual/data/characters.csv"

# Ruta del archivo SQLite que se creará
DATABASE_PATH = "C:/Users/Pedro/Desktop/M-Pindividual/data/database.db"

# Función para convertir un CSV en una tabla de SQLite
def csv_to_sqlite(csv_file, table_name, db_path):
    df = pd.read_csv(csv_file)

    # Conectar a SQLite (se crea el archivo si no existe)
    conn = sqlite3.connect(db_path)

    # Guardar el DataFrame como una tabla en SQLite
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Cerrar la conexión
    conn.close()

    print(f"Datos de {csv_file} cargados a la tabla {table_name} en {db_path}")

# Convertir los CSV a SQLite
def convert():
    csv_to_sqlite(MOVIES_CSV, "movies", DATABASE_PATH)
    csv_to_sqlite(DIRECTORS_CSV, "directors", DATABASE_PATH)
    csv_to_sqlite(CHARACTERS_CSV, "characters", DATABASE_PATH)

if __name__ == "__main__":
    convert()
