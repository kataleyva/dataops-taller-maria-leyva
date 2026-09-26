import sqlite3

import pandas as pd

columnas_esperadas = {
    "id": "INTEGER",
    "fecha": "TEXT",
    "producto": "TEXT",
    "categoria": "TEXT",
    "cantidad": "INTEGER",
    "precio_unitario": "REAL",
    "cliente_id": "INTEGER",
}


def test_tabla_tiene_columnas_esperadas(ventas_crudas):
    # La tabla ventas tiene exactamente las columnas esperadas.
    assert list(ventas_crudas.columns) == list(columnas_esperadas)


def test_esquema_tipos_de_columnas(ruta_db):
    # Los tipos de dato en SQLite coinciden con el esquema definido.
    conn = sqlite3.connect(ruta_db)
    try:
        info = conn.execute("PRAGMA table_info(ventas)").fetchall()
    finally:
        conn.close()
    tipos = {columna[1]: columna[2] for columna in info}
    assert tipos == columnas_esperadas


def test_cantidad_no_negativa(ventas_crudas):
    # Ninguna cantidad es negativa (los nulos se ignoran).
    assert (ventas_crudas["cantidad"] < 0).sum() == 0


def test_precio_unitario_mayor_que_cero(ventas_crudas):
    # Todos los precios son mayores que 0 (los nulos se ignoran).
    assert (ventas_crudas["precio_unitario"] <= 0).sum() == 0


def test_no_hay_fechas_futuras(ventas_crudas):
    # Ninguna venta tiene fecha posterior a hoy.
    fechas = pd.to_datetime(ventas_crudas["fecha"])
    assert (fechas > pd.Timestamp.today()).sum() == 0


def test_fechas_con_formato_valido(ventas_crudas):
    # Todas las fechas cumplen el formato YYYY-MM-DD.
    assert ventas_crudas["fecha"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all()