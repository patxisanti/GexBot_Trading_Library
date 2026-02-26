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
        if len(df) < 2: return
        
        actual = df.iloc[-1]
        previo = df.iloc[-2]
        
        spot = actual['spot']
        zg = actual['zero_gamma']
        
        # Lógica de Rotura: El precio cruza el Zero Gamma
        rompe_arriba = previo['spot'] <= zg and spot > zg
        rompe_abajo = previo['spot'] >= zg and spot < zg
        
        if rompe_arriba or rompe_abajo:
            tipo = "🚀 ROTURA ALCISTA (Hacia Long Gamma)" if rompe_arriba else "⚠️ ROTURA BAJISTA (Hacia Short Gamma)"
            msg = (f"**6 - ALERTA DE ROTURA**\n"
                   f"• Tipo: {tipo}\n"
                   f"• Precio: {spot:.2f} | Zero Gamma: {zg:.2f}\n"
                   f"• Info: El precio ha cruzado el eje de equilibrio.")
            requests.post(DISCORD_WEBHOOK, json={"content": msg})
    except: pass

if __name__ == "__main__": analizar()
