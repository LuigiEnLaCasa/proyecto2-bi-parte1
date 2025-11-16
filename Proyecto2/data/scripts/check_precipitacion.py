import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT  / "RawData2021" / "Precipitacion" / "OAB - PMPLL - La Ciudad.csv"

df = pd.read_csv(SRC, sep=None, engine="python", dtype=str, encoding="utf-8")
print("shape:", df.shape)
print("cols:", list(df.columns))
print("dups:", df.duplicated().sum())
print("nulos top:\n", df.isna().sum().sort_values(ascending=False).head(10))
print(df.head())