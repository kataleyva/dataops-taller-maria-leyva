import numpy as np
import pandas as pd
import pytest

from src.transform import aggregate_sales, calculate_metrics, clean_data


@pytest.fixture
def ventas_ejemplo():
    # Dataframe pequeño con pocos registros realizado por AI
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "fecha": ["2025-01-15", "2025-01-15", "2025-02-10", "2025-02-20"],
            "producto": ["Mouse", "Mouse", "Jean", "Balón"],
            "categoria": ["Electrónica", "Electrónica", "Ropa", "Deportes"],
            "cantidad": [2, 2, np.nan, 3],
            "precio_unitario": [10.0, 10.0, 40.0, np.nan],
            "cliente_id": [7, 7, 8, 9],
        }
    )


def test_clean_data_elimina_duplicados(ventas_ejemplo):
    # Debe quedar un registro porque registros 1 y 2 son iguales
    resultado = clean_data(ventas_ejemplo)
    assert len(resultado) == 3


def test_clean_data_rellena_cantidad_con_cero(ventas_ejemplo):
    # La cantidad nula se reemplaza por 0.
    resultado = clean_data(ventas_ejemplo)
    fila = resultado[resultado["producto"] == "Jean"]
    assert fila["cantidad"].iloc[0] == 0
    assert resultado["cantidad"].isna().sum() == 0


def test_clean_data_rellena_precio_con_media(ventas_ejemplo):
    # El precio nulo se reemplaza por la media: (10 + 40) / 2 = 25.
    resultado = clean_data(ventas_ejemplo)
    fila = resultado[resultado["producto"] == "Balón"]
    assert fila["precio_unitario"].iloc[0] == pytest.approx(25.0)
    assert resultado["precio_unitario"].isna().sum() == 0


def test_clean_data_convierte_fecha(ventas_ejemplo):
    # La columna fecha queda como tipo datetime.
    resultado = clean_data(ventas_ejemplo)
    assert pd.api.types.is_datetime64_any_dtype(resultado["fecha"])


def test_clean_data_no_modifica_original(ventas_ejemplo):
    # clean_data trabaja sobre una copia y no altera el DataFrame original.
    original = ventas_ejemplo.copy()
    clean_data(ventas_ejemplo)
    pd.testing.assert_frame_equal(ventas_ejemplo, original)


def test_calculate_metrics_venta_total(ventas_ejemplo):
    # venta_total = cantidad * precio_unitario.
    resultado = calculate_metrics(clean_data(ventas_ejemplo))
    esperado = resultado["cantidad"] * resultado["precio_unitario"]
    pd.testing.assert_series_equal(
        resultado["venta_total"], esperado, check_names=False
    )
    mouse = resultado[resultado["producto"] == "Mouse"]
    assert mouse["venta_total"].iloc[0] == pytest.approx(20.0)


def test_calculate_metrics_extrae_mes(ventas_ejemplo):
    # La columna mes corresponde al mes de la fecha.
    resultado = calculate_metrics(clean_data(ventas_ejemplo))
    assert resultado["mes"].tolist() == [1, 2, 2]


def test_aggregate_sales_agrupa_por_categoria_y_mes():
    # Suma venta_total por cada combinación de categoria y mes.
    df = pd.DataFrame(
        {
            "categoria": ["Ropa", "Ropa", "Ropa", "Hogar"],
            "mes": [1, 1, 2, 1],
            "venta_total": [10.0, 5.0, 7.0, 3.0],
        }
    )
    resultado = aggregate_sales(df)

    assert len(resultado) == 3
    ropa_enero = resultado[(resultado["categoria"] == "Ropa") & (resultado["mes"] == 1)]
    assert ropa_enero["venta_total"].iloc[0] == pytest.approx(15.0)