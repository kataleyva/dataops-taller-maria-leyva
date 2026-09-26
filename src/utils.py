from pathlib import Path


def save_to_csv(df, path):
    # Guarda dtatframe en un csv
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
