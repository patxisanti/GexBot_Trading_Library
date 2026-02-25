import pandas as pd
import requests
import os
import sys
import time
from datetime import datetime
import pytz

sys.path.append(os.path.expanduser('~/GexBot_Trading_Library'))
from config import API_KEY, ACTIVOS, TIMEZONE_LOCAL, PAUSA_API

def recolectar_triple_horizonte():
    tz = pytz.timezone(TIMEZONE_LOCAL)
    ahora = datetime.now(tz)
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    ts = ahora.strftime("%H:%M:%S")

    print(f"🚀 [{ts}] Captura Triple (0DTE, 1DTE, 90D)...")

    for ticker in ACTIVOS:
        # Añadimos '1d' a la lista de modos
        for modo in ["zero", "1d", "90d"]: 
            url = f"https://api.gexbot.com/{ticker}/state/{modo}?key={API_KEY}"
            try:
                r = requests.get(url, timeout=10)
                data = r.json()

                if data and data.get('zero_gamma') != 0 and data.get('zero_gamma') is not None:
                    df = pd.DataFrame([data])
                    # Etiquetado preciso para el Backtesting
                    df['tipo_dato'] = "SWING_90D" if modo == "90d" else ("PROX_DIA_1DTE" if modo == "1d" else "INTRADIA_0DTE")
                    df['hora_canarias'] = ts
                    
                    ruta_carpeta = f"01_Backtesting_JSON/{ticker}"
                    if not os.path.exists(ruta_carpeta): os.makedirs(ruta_carpeta)
                    
                    ruta_archivo = f"{ruta_carpeta}/{ticker}_{fecha_hoy}.csv"
                    df.to_csv(ruta_archivo, mode='a', header=not os.path.exists(ruta_archivo), index=False)
                
                time.sleep(PAUSA_API)
            except: continue

    print(f"✅ [{ts}] Ronda completada.")

if __name__ == "__main__":
    recolectar_triple_horizonte()
