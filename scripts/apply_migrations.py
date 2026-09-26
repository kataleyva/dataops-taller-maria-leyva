import hashlib
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent.parent
migrations_dir = root / "migrations"
default_db = root / "data" / "ventas_migraciones.db"


def obtener_historial(conn):
    #Creación de tabla con historial
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_history (
            version TEXT PRIMARY KEY,
            archivo TEXT NOT NULL,
            checksum TEXT NOT NULL,
            aplicada_en TEXT NOT NULL
        )
        """)
    filas = conn.execute("SELECT version, checksum FROM schema_history")
    return dict(filas.fetchall())


def aplicar_migraciones(db_path=default_db):
    #Aplicacion de migraciones pendientes
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        historial = obtener_historial(conn)
        for archivo in sorted(migrations_dir.glob("V*.sql")):
            version = archivo.name.split("_")[0]
            sql = archivo.read_text(encoding="utf-8")
            checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()

            if version in historial:
                if historial[version] != checksum:
                    raise RuntimeError(
                        f"{archivo.name} fue modificada después de aplicarse. "
                    )
                print(f"  = {archivo.name} ya aplicada")
                continue

            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_history VALUES (?, ?, ?, ?)",
                (
                    version,
                    archivo.name,
                    checksum,
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                ),
            )
            conn.commit()
            print(f"  + {archivo.name} aplicada")
    finally:
        conn.close()


if __name__ == "__main__":
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else default_db
    print(f"Aplicando migraciones en {destino}")
    aplicar_migraciones(destino)