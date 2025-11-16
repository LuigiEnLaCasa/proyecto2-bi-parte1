# scripts/temperatura.py (Paso 1)
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"RawData2021"/"Temperatura"/"temperaturas.csv"

df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")


####
## Exploración de los datos
####


# Evaluar el tamaño del dataset
print("shape:", df.shape)
print("cols:", list(df.columns))

# Evaluar Duplicados y nulos
print("\nDuplicados:", df.duplicated().sum())
print("\nNulos por columna:")
print(df.isna().sum())


# tipos y calendario
an = pd.to_numeric(df["Año"], errors="coerce")
ms = pd.to_numeric(df["Mes"], errors="coerce")

print("\nAño no numéricos:", an.isna().sum())
print("Mes no numéricos:", ms.isna().sum())
print("Mes fuera de 1..12:", (~ms.between(1,12)).sum())

# chequeo unicidad año-mes
dups_y_m = pd.Series(list(zip(an, ms))).duplicated().sum()
print("Duplicados (Año,Mes):", dups_y_m)


print("\nValores únicos en 'Mes':")
print(df["Mes"].unique()[:20])


####
## Transformaciones 
####



# Paso 4: Mes → número
mes_map = {
    "Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6,
    "Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12
}

# Crear columnas mes_nombre, mes_num y fecha_mes

df["mes_nombre"] = df["Mes"].str.strip()
df["mes_num"] = df["Mes"].map(mes_map).astype(int)

df["fecha_mes"] = pd.to_datetime(
    df["Año"].astype(str) + "-" + df["mes_num"].astype(str) + "-01",
    errors="coerce"
)

# --------- AÑADIDO: filtrar solo 2021 y validar meses ----------
pre_rows = len(df)
df = df[df["Año"].astype(str) == "2021"].copy()
post_rows = len(df)
print(f"\nFiltrado por Año==2021: se eliminaron {pre_rows - post_rows} filas; quedan {post_rows}.")

# quitar meses fuera de 1..12 si existiera algún error
invalid_months = (~df["mes_num"].between(1,12)).sum()
if invalid_months:
    df = df[df["mes_num"].between(1,12)].copy()
    print(f"Meses fuera de 1..12 eliminados: {invalid_months}")

# ordenar y resetear índice
df.sort_values(["Año","mes_num"], inplace=True)
df.reset_index(drop=True, inplace=True)
# ---------------------------------------------------------------

# --------- Revisión de duplicados en mes_num ----------
dups = df[df.duplicated(subset=["mes_num"], keep=False)]
if not dups.empty:
    print("\n  Se encontraron duplicados en 'mes_num':")
    print(dups[["Año", "mes_num", "mes_nombre", "Temperatura promedio"]])
    # eliminar duplicados manteniendo el primero
    df = df.drop_duplicates(subset=["mes_num"], keep="first").copy()
    print(f"\n Duplicados eliminados. Filas restantes: {len(df)}")
else:
    print("\n No hay duplicados en 'mes_num'. Todo correcto (12 meses esperados).")


# Crear carpeta CleanData2021 y guardar CSV limpio
OUT_DIR = ROOT / "CleanData2021"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "temperatura_2021.csv"

df.to_csv(OUT_FILE, index=False, encoding="utf-8")
print(f"\nCHECK- Archivo limpio guardado en: {OUT_FILE}")
print(df[["Año","mes_nombre","mes_num","fecha_mes"]].head())