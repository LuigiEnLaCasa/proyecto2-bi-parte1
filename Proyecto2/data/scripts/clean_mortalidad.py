# scripts/mortalidad_inspect.py — Paso 1: explorar formato
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"RawData2021"/"Mortalidad"/"MortalidadPrematura2021.csv"

df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")

print("shape:", df.shape)
print("cols:", list(df.columns))

print("\nDuplicados:", df.duplicated().sum())
print("\nNulos por columna (top 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))

# año/mes deben ser 2021 y 1..12
an = pd.to_numeric(df.get("ANO"), errors="coerce")
ms = pd.to_numeric(df.get("MES"), errors="coerce")
print("\nAño únicos:", sorted(an.dropna().unique().tolist())[:10])
print("Mes fuera de 1..12:", (~ms.between(1,12)).sum() if ms.notna().any() else "NA")

# Chequeo rápido de categorías clave
for c in ["SEXO","REGIMEN_SEGURIDAD_SOCIAL","LOCALIDAD","CIE10_AGRUPADA"]:
    if c in df.columns:
        vals = df[c].dropna().astype(str).str.strip().str[:30].unique()[:10]
        print(f"\nEjemplos {c}:", vals)

print("\nMuestra:")
print(df.head())