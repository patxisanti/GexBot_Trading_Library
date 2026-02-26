# -*- coding: utf-8 -*-
import pandas as pd
import requests
from datetime import datetime
from config import DISCORD_WEBHOOK

def analizar():
    f = datetime.now().strftime("%Y-%m-%d")
    archivo = f"/root/GexBot_Trading_Library/01_Backtesting_JSON/SPX/SPX_{f}_rt.csv"
    try:
        df = pd.read_csv(archivo)
        gex = df['gex_total_vol'].iloc[-1]
        bando = "CIAN 🔵 (Alcista/Estable)" if gex > 0 else "MAGENTA 🔴 (Bajista/Volátil)"
        msg = f"**1 - ESCENARIO GEX SPX**\n• Bando actual: {bando}\n• GEX Total: {gex:.0f}"
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
    except: pass

if __name__ == "__main__": analizar()
