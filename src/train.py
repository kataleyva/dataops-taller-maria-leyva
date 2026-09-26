from pathlib import Path
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.extract import extract_data
from src.transform import aggregate_sales, calculate_metrics, clean_data
from src.utils import save_to_csv

root = Path(__file__).resolve().parent.parent
db_path = root / "data" / "ventas.db"
csv_path = root / "data" / "agreggated_sales.csv"
model_path = root / "models" / "model.pkl"


def train_model(df, model_path=model_path):
    # Entrenamiento de regresión de ventas por mes
    ventas_mes = df.groupby("mes", as_index=False)["venta_total"].sum()
    features = ventas_mes[["mes"]]
    target = ventas_mes["venta_total"]

    model = LinearRegression()
    model.fit(features, target)
    r2 = model.score(features, target)

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return model, r2


def run_pipeline():
    # Ejecución del pipeline
    df = extract_data(db_path)
    df = calculate_metrics(clean_data(df))
    aggregated = aggregate_sales(df)
    save_to_csv(aggregated, csv_path)

    model, r2 = train_model(aggregated)
    siguiente_mes = int(aggregated["mes"].max()) + 1
    prediccion = model.predict(pd.DataFrame({"mes": [siguiente_mes]}))[0]

    print(f"Registros limpios: {len(df)}")
    print(f"Reporte guardado en: {csv_path}")
    print(f"Modelo guardado en: {model_path}")
    print(f"R2 del modelo: {r2:.3f}")
    print(f"Prediccion de ventas para el mes {siguiente_mes}: {prediccion:,.2f}")


if __name__ == "__main__":
    run_pipeline()
