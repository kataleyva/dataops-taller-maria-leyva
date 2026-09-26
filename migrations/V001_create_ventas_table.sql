CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    producto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    cantidad INTEGER,
    precio_unitario REAL,
    cliente_id INTEGER NOT NULL
);