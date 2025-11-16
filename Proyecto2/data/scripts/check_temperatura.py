# scripts/check_temperatura_tipos.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "RawData2021" / "Temperatura" / "temperaturas.csv"

# --- Carga segura ---
df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")

print("\n Archivo leído correctamente.")
print("Filas, Columnas:", df.shape)

print("\nColumnas:")
print(list(df.columns))

print("\nTipos de datos detectados:")
print(df.dtypes)

print("\nDuplicados:", df.duplicated().sum())

print("\nValores nulos por columna (top 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))

print("\nVista rápida de los datos:")
print(df.head())

# Si tiene alguna columna de fecha o periodo, mostramos ejemplos
print("\nValores de ejemplo (posibles fechas o periodos):")
for col in df.columns:
    if "fecha" in col.lower() or "periodo" in col.lower():
        print(f"\nColumna: {col}")
        print(df[col].head(10).to_list())