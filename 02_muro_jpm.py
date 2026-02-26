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
        spot = df['spot'].iloc[-1]
        msg = f"**2 - MURO JPM**\n• Precio Actual: {spot:.2f}\n• Muro Call: 7000.00\n• Muro Put: 6330.00"
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
    except: pass

if __name__ == "__main__": analizar()
