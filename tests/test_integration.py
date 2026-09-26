import pytest

from src.extract import extract_data
from src.train import train_model
from src.transform import aggregate_sales, calculate_metrics, clean_data


def test_pipeline_extraer_transformar_agregar(ruta_db):
    # extract, clean, metrics, aggregate produce un resultado válido.
    df = extract_data(ruta_db)
    df = calculate_metrics(clean_data(df))
    resultado = aggregate_sales(df)

    assert not resultado.empty
    assert list(resultado.columns) == ["categoria", "mes", "venta_total"]
    assert resultado.isna().sum().sum() == 0


def test_pipeline_entrena_modelo(ruta_db, tmp_path):
    # El pipeline completo entrena y guarda un modelo.
    df = calculate_metrics(clean_data(extract_data(ruta_db)))
    ruta_modelo = tmp_path / "model.pkl"

    _, r2 = train_model(aggregate_sales(df), model_path=ruta_modelo)

    assert ruta_modelo.exists()
    assert r2 <= 1.0


def test_extract_falla_si_no_existe_la_base(tmp_path):
    # extract_data lanza FileNotFoundError si la base de datos no existe.
    with pytest.raises(FileNotFoundError):
        extract_data(tmp_path / "no_existe.db")