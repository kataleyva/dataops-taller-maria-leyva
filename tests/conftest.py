import pytest

from scripts.create_db import crear_base_datos, db_path
from src.extract import extract_data


@pytest.fixture(scope="session")
def ruta_db():
    # Garantización de que base de datos existe 
    if not db_path.exists():
        crear_base_datos()
    return db_path


@pytest.fixture(scope="session")
def ventas_crudas(ruta_db):
    # Datos de la tabla de ventas en crudo
    return extract_data(ruta_db)