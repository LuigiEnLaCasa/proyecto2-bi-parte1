import pandas as pd
from pathlib import Path

# --- Rutas ---
ROOT = Path(__file__).resolve().parents[1]
PM25_DIR = ROOT / "RawData2021" / "PM25"

# --- Archivos ---
files = ["IBOCA-PM25-2021-1.xlsx", "IBOCA-PM25-2021-2.xlsx"]

for f in files:
    path = PM25_DIR / f
    print(f"\n Revisando: {f}")

    # --- Carga robusta ---
    df = pd.read_excel(path, dtype=str)

    print("Filas, Columnas:", df.shape)
    print("Columnas:", list(df.columns)[:15])  # primeras 15 por si son muchas

    print("\nDuplicados:", df.duplicated().sum())
    print("Nulos por columna (top 10):")
    print(df.isna().sum().sort_values(ascending=False).head(10))

    print("\nVista rápida:")
    print(df.head())

    print("-" * 60)

