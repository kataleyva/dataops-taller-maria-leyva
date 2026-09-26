import shutil
from datetime import date
from pathlib import Path

root = Path(__file__).resolve().parent.parent
db_path = root / "data" / "ventas.db"
snpashots_dir = root / "data" / "snapshots"


def crear_snapshot(db_path=db_path, destino=snpashots_dir):
    # Copia de base de datos
    if not db_path.exists():
        raise FileNotFoundError(f"No se encontró la base de datos: {db_path}")

    destino.mkdir(parents=True, exist_ok=True)
    snapshot = destino / f"ventas_{date.today():%Y%m%d}.db"
    shutil.copy2(db_path, snapshot)
    return snapshot


if __name__ == "__main__":
    ruta = crear_snapshot()
    print(f"Snapshot creado en {ruta}")