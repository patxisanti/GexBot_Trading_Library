import pandas as pd
import requests
import os
import sys
import json
from datetime import datetime
import pytz

BASE_DIR = "/root/GexBot_Trading_Library"
BACKTEST_DIR = os.path.join(BASE_DIR, "01_Backtesting_JSON")
sys.path.append(BASE_DIR)
from config import API_KEY, ACTIVOS, TIMEZONE_LOCAL

def recolectar():
    tz = pytz.timezone(TIMEZONE_LOCAL)
    ahora = datetime.now(tz)
    ts = ahora.strftime("%H:%M:%S")
    fecha_hoy = ahora.strftime("%Y-%m-%d")

    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"🚀 [{ts}] Sincronizando Búnker (Modo: Real-Time Zero)...")

    for ticker in ACTIVOS:
        url = f"https://api.gexbot.com/{ticker}/state/zero?key={API_KEY}"
        try:
            r = requests.get(url, headers=headers, timeout=12)
            
            if r.status_code == 200:
                data = r.json()
                if data:
                    ruta_ticker = os.path.join(BACKTEST_DIR, ticker)
                    os.makedirs(ruta_ticker, exist_ok=True)
                    
                    # Guardar JSON con sufijo RT (Real Time)
                    with open(os.path.join(ruta_ticker, f"{ticker}_{fecha_hoy}_rt.json"), 'a') as f:
                        f.write(json.dumps(data) + "\n")
                    
                    # Extraer métricas clave (ajustado a tu JSON real)
                    gex_total = data.get('sum_gex_vol', 0)
                    z_gamma = data.get('zero_gamma', 0)
                    spot = data.get('spot', 0)
                    
                    # Guardar CSV
                    df = pd.DataFrame([{
                        'timestamp': ts,
                        'spot': spot,
                        'gex_total_vol': gex_total,
                        'zero_gamma': z_gamma
                    }])
                    ruta_csv = os.path.join(ruta_ticker, f"{ticker}_{fecha_hoy}_rt.csv")
                    df.to_csv(ruta_csv, mode='a', header=not os.path.exists(ruta_csv), index=False)
                    
                    print(f"  ✅ {ticker} | Spot: {spot} | GEX Vol: {gex_total} | Z-Gamma: {z_gamma}")
                else:
                    print(f"  ⚠️ {ticker} | Respuesta vacía.")
            elif r.status_code == 400:
                print(f"  ❌ {ticker} | No disponible en este endpoint (Skip)")
            else:
                print(f"  ❌ {ticker} | Error HTTP {r.status_code}")
        except Exception as e:
            print(f"  🔥 {ticker} | Error de red: {str(e)}")

    print(f"🏁 Ronda completada con éxito.")

if __name__ == "__main__":
    recolectar()
