import pandas as pd


def clean_data(df):
    # Limpia dataframe de ventas (Elimina duplicados y rellena nulos)
    df = df.copy()
    columnas = [col for col in df.columns if col != "id"]
    df = df.drop_duplicates(subset=columnas)
    df["cantidad"] = df["cantidad"].fillna(0).astype(int)
    df["precio_unitario"] = df["precio_unitario"].fillna(df["precio_unitario"].mean())
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df.reset_index(drop=True)


def calculate_metrics(df):
    # Agregación de columnas calculadas
    df = df.copy()
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]
    df["mes"] = df["fecha"].dt.month
    return df


def aggregate_sales(df):
    # Agrupación de categorías y mes sumando venta_total
    return df.groupby(["categoria", "mes"], as_index=False)["venta_total"].sum()
