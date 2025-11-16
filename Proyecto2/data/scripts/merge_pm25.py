# scripts/merge_pm25.py
# Une PM25_2021_1_hourly.csv y PM25_2021_2_hourly.csv en un solo archivo consolidado
import pandas as pd
from pathlib import Path

# --- Rutas ---
ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "processed"
OUT_FILE = IN_DIR / "PM25_2021_hourly.csv"

# --- Archivos a unir ---
FILES = [
    IN_DIR / "PM25_2021_1_hourly.csv",
    IN_DIR / "PM25_2021_2_hourly.csv"
]

# --- Leer y concatenar ---
dfs = []
for f in FILES:
    print(f"📄 Leyendo: {f.name}")
    df = pd.read_csv(f, encoding="utf-8")
    dfs.append(df)

# Combinar y limpiar duplicados si los hay
merged = pd.concat(dfs, ignore_index=True)
merged.drop_duplicates(inplace=True)

# Ordenar por fecha y estación
merged["fecha_hora"] = pd.to_datetime(merged["fecha_hora"], errors="coerce")
merged.sort_values(["fecha_hora", "estacion"], inplace=True)

# Guardar CSV final
merged.to_csv(OUT_FILE, index=False, encoding="utf-8")

print(f"\n✅ Archivo unificado guardado en: {OUT_FILE}")
print(f"Total filas: {len(merged)} | Estaciones: {merged['estacion'].nunique()}")
print(merged.head())