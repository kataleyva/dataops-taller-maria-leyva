# Creación de base de datos simulada de SQLite para datos de ventas.

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

seed = 42
num_registros = 200
nulos = 6
num_duplicados = 8

root = Path(__file__).resolve().parent.parent
db_path = root / "data" / "ventas.db"

#Creación de variación de productors y precios con AI
productos  = {
    "Electrónica": [("Audífonos", 80.0), ("Mouse", 25.0), ("Teclado", 45.0)],
    "Ropa": [("Camiseta", 15.0), ("Jean", 40.0), ("Chaqueta", 70.0)],
    "Hogar": [("Lámpara", 30.0), ("Cojín", 12.0), ("Sartén", 35.0)],
    "Deportes": [("Balón", 20.0), ("Mancuernas", 50.0), ("Yoga mat", 28.0)],
}

def generar_registros():
    #Ventas simuladas
    inicio = date(2025,1,1)
    registros = []
    for i in range(num_registros):
        fecha = inicio + timedelta(days=random.randint(0,364))
        categoria = random.choice(list(productos.keys()))
        producto, precio_unitario = random.choice(productos[categoria])
        cantidad = random.randint(1, 10)
        cliente_id = random.randint(1, 50)
        registros.append([fecha.isoformat(), producto, categoria, cantidad, precio_unitario, cliente_id])


    #Valores nulos:
    indices = random.sample(range(num_registros), nulos)
    for i in indices [: nulos//2]:
        registros[i][3] = None
    for i in indices[nulos//2:]:
        registros[i][4] = None

    #Valores duplicados:
    registros.extend(list(fila) for fila in random.sample(registros, num_duplicados))
    return registros

def crear_base_datos():
    #Creación de tabla de ventas vacía y luego inserta registros
    random.seed(seed)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.unlink(missing_ok=True)

    conn = sqlite3.connect(db_path)

    try: 
        conn.execute("""
            CREATE TABLE ventas (
                id INTEGER PRIMARY KEY,
                fecha TEXT NOT NULL,
                producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                cantidad INTEGER,
                precio_unitario REAL,
                cliente_id INTEGER NOT NULL
            )
            """)
        conn.executemany(
            "INSERT INTO ventas (fecha, producto, categoria, cantidad, precio_unitario, cliente_id) VALUES (?, ?, ?, ?, ?, ?)",
            generar_registros(),
        )
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    crear_base_datos()
