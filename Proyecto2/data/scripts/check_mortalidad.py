#Vamos a evaluar el archivo MortalidadPrematura2021.csv
import pandas as pd
from pathlib import Path

#Rutas
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "RawData2021" / "Mortalidad" / "MortalidadPrematura2021.csv"

# Carga segura 
df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")

print("\nArchivo cargado correctamente")
print("Filas, Columnas:", df.shape)
print("\nColumnas:")
print(list(df.columns))

#Checks básicos 
print("\nDuplicados:", df.duplicated().sum())
print("\nValores nulos por columna (top 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))

# Muestra 5 registros 
print("\nVista rápida de los datos:")
print(df.head())

# Tipos esperados (sin convertir aún)
for col in ["ANO", "MES", "EDAD_FALLECIDO"]:
    if col in df.columns:
        bad = pd.to_numeric(df[col], errors="coerce").isna().sum()
        print(f"{col}: {bad} valores no numéricos")