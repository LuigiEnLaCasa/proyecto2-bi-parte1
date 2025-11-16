# scripts/clean_pm25_check.py — Paso 1: exploración básica
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"formated"/"PM25_2021_hourly.csv"

df = pd.read_csv(SRC, sep=",", dtype=str, encoding="utf-8")

print("shape:", df.shape)
print("cols:", list(df.columns))

# duplicados y nulos
print("\nDuplicados:", df.duplicated().sum())
print("\nNulos por columna:")
print(df.isna().sum())

# vista rápida
print("\nVista rápida:")
print(df.head())


# ---- Limpieza de nulos ----
pre_rows = len(df)
df = df.dropna(subset=["pm25_concentracion", "pm25_media_movil", "iboca"], how="any").copy()
post_rows = len(df)
print(f"\n✅ Filas eliminadas por nulos: {pre_rows - post_rows} | Filas restantes: {post_rows}")

# ---- Verificar fechas ----
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], errors="coerce")
years = df["fecha_hora"].dt.year.unique()
print("\nAños únicos detectados:", years)

# ---- Revisión final: nulos y duplicados ----
print("\nRevisión final de nulos:")
print(df.isna().sum())

dups = df.duplicated().sum()
print(f"\nDuplicados totales: {dups}")

if dups > 0:
    df = df.drop_duplicates().copy()
    print(f"✅ Duplicados eliminados. Filas restantes: {len(df)}")
else:
    print("✅ No hay duplicados, dataset limpio.")   

# (añade al final)
# Mantener solo 2021 (por si quedó 2022)
df = df[df["fecha_hora"].dt.year == 2021].copy()

# ---- Chequeo de valores imposibles (diagnóstico; no modifica df) ----
import numpy as np
bounds = {
    "pm25_concentracion": (0, 500),
    "pm25_media_movil":   (0, 500),
    "iboca":              (0, 500),
}
for col, (lo, hi) in bounds.items():
    v = pd.to_numeric(df[col], errors="coerce")
    print(f"\n[{col}] estadísticas (solo 2021):")
    print(f"  n={v.notna().sum()}  min={v.min()}  p01={v.quantile(0.01)}  p50={v.median()}  p99={v.quantile(0.99)}  max={v.max()}")
    out_lo = (v < lo).sum()
    out_hi = (v > hi).sum()
    nans  = v.isna().sum()
    print(f"  Fuera de rango  <{lo}: {out_lo}   >{hi}: {out_hi}   NaN tras parseo: {nans}")

# 2) Orden por fecha, luego estación
df2 = df.sort_values(["fecha_hora","estacion"]).reset_index(drop=True)

# asegurar carpeta de salida
(Path(ROOT/"CleanData2021")).mkdir(parents=True, exist_ok=True)

(df2).to_csv(ROOT/"CleanData2021"/"PM25_2021.csv", index=False, encoding="utf-8")

print("✓ Archivos ordenados guardados.")