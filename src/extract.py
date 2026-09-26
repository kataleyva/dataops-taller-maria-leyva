import sqlite3
from pathlib import Path 
import pandas as pd

def extract_data(db_path):
    #Lee la tabla y retorn dataframe
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"No se encontró la base de datos: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query("SELECT * FROM ventas", conn)
    except (sqlite3.Error, pd.errors.DatabaseError) as exc:
            raise RuntimeError(f"Error al leer tabla de ventas: {exc}") from exc
    finally: conn.close()