# scripts/pm25_excel_to_csv.py
import pandas as pd
from pathlib import Path
import unicodedata, re


#CAMBIA LA INFORMACIÓN DE AQUÍ SI QUERES VOLVER A HACER SESTE PROCESO BRO
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT /  "RawData2021" / "PM25" / "IBOCA-PM25-2021-1.xlsx"
OUT_DIR = ROOT /  "fromated"; OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "PM25_2021_1_hourly.csv"

def norm(s):
    s = str(s)
    s = "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", s.strip().lower())

def comma_to_float(x):
    if isinstance(x, str):
        x = x.strip()
        if x == "" or x.lower().startswith("sin data"): return None
        return x.replace(",", ".")
    return x

def tidy_from_excel(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, header=None, dtype=str)

    stations_row = 4   # fila 5 (0-index)
    subcols_row   = 6  # fila 7 (0-index)

    stations = raw.iloc[stations_row].ffill(axis=0).reset_index(drop=True)
    subcols  = raw.iloc[subcols_row].reset_index(drop=True)
    data     = raw.iloc[subcols_row+1:].reset_index(drop=True)

    # detectar la columna de fecha por nombre
    fecha_idx = 0
    for j, name in enumerate(subcols):
        if "fecha" in norm(name):
            fecha_idx = j; break

    frames = []
    j = fecha_idx + 1
    n = data.shape[1]

    while j + 2 < n:
        # validar que el trío sea Concentración / Media móvil / IBOCA
        trio_norm = [norm(x) for x in subcols.iloc[j:j+3]]
        if not ("concentr" in trio_norm[0] and "media" in trio_norm[1] and "iboca" in trio_norm[2]):
            j += 1
            continue

        est = str(stations.iloc[j]).strip() or "Estacion_desconocida"
        sub = data.iloc[:, [fecha_idx, j, j+1, j+2]].copy()
        sub.columns = ["fecha_hora", "pm25_concentracion", "pm25_media_movil", "iboca"]
        sub["estacion"] = est
        frames.append(sub)
        j += 3

    tidy = pd.concat(frames, ignore_index=True)

    for c in ["pm25_concentracion", "pm25_media_movil", "iboca"]:
        tidy[c] = tidy[c].apply(comma_to_float)
        tidy[c] = pd.to_numeric(tidy[c], errors="coerce")

    tidy["fecha_hora"] = pd.to_datetime(tidy["fecha_hora"], errors="coerce", dayfirst=True)
    tidy = tidy.dropna(subset=["fecha_hora"])
    return tidy[["fecha_hora","estacion","pm25_concentracion","pm25_media_movil","iboca"]]

if __name__ == "__main__":
    df = tidy_from_excel(IN_FILE)
    df.sort_values(["fecha_hora","estacion"], inplace=True)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"✓ CSV: {OUT_FILE}")
    print(f"Filas: {len(df)} | Estaciones: {df['estacion'].nunique()}")
    print(df.head())