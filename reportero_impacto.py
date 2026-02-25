import pandas as pd
import requests
import os
from datetime import datetime
from config import DISCORD_WEBHOOK, ACTIVOS

BASE_DIR = "/root/GexBot_Trading_Library"
BACKTEST_DIR = os.path.join(BASE_DIR, "01_Backtesting_JSON")

def enviar_discord(mensaje):
    payload = {"content": f"### 🛡️ SENTINEL AUTOPSIA RTH\n{mensaje}"}
    requests.post(DISCORD_WEBHOOK, json=payload)

def analizar():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    reporte = []
    
    for ticker in ['SPX', 'NDX', 'QQQ', 'IWM', 'SPY']:
        ruta_csv = os.path.join(BACKTEST_DIR, ticker, f"{ticker}_{fecha_hoy}_rt.csv")
        if os.path.exists(ruta_csv):
            df = pd.read_csv(ruta_csv)
            if not df.empty:
                last = df.iloc[-1]
                first = df.iloc[0]
                diff_gex = last['gex_total_vol'] - first['gex_total_vol']
                tendencia = "📈" if diff_gex > 0 else "📉"
                
                linea = (f"**{ticker}**: Spot {last['spot']} | "
                         f"GEX: {last['gex_total_vol']:.2f} ({tendencia}) | "
                         f"Z-Gamma: {last['zero_gamma']}")
                reporte.append(linea)
    
    if reporte:
        enviar_discord("\n".join(reporte))
    else:
        enviar_discord("⚠️ Error Crítico: No se encontraron datos para la autopsia de hoy.")

if __name__ == "__main__":
    analizar()
