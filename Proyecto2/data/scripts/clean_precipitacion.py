# scripts/precipitacion.py — Paso 1: inspección básica
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"Formated"/"Precipitacion2021.csv"

###
## Exploración básica
###

df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")

print("shape:", df.shape)
print("cols:", list(df.columns))

# Paso 2: revisión de duplicados y nulos
print("\nDuplicados:", df.duplicated().sum())
print("\nNulos por columna:")
print(df.isna().sum())

print("\nEjemplos de Periodo:")
print(df["Periodo"].head(10))

# convertir a fecha
df["Periodo_dt"] = pd.to_datetime(df["Periodo"], format="%Y-%m", errors="coerce")

# verificar años distintos
print("\nAños únicos detectados:", df["Periodo_dt"].dt.year.unique())


##
# Transformaciones
##

# ---- Filtro 2021 + normalización y guardado ----
pre = len(df)
df_2021 = df[df["Periodo_dt"].dt.year == 2021].copy()
print(f"\nFiltrado a 2021: {pre - len(df_2021)} filas eliminadas; quedan {len(df_2021)}.")

# fecha_mes y valor numérico
df_2021["fecha_mes"] = df_2021["Periodo_dt"].dt.to_period("M").dt.to_timestamp()
df_2021["precipitacion_mm"] = pd.to_numeric(df_2021["Valor"], errors="coerce")

# ordenar y columnas finales
df_2021 = df_2021[["fecha_mes", "precipitacion_mm"]].sort_values("fecha_mes").reset_index(drop=True)

# guardar en CleanData2021
OUT_DIR = ROOT / "CleanData2021"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "precipitacion_2021.csv"
df_2021.to_csv(OUT_FILE, index=False, encoding="utf-8")

print(f"✅ Archivo limpio guardado en: {OUT_FILE}")
print(df_2021.head())