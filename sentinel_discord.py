import pandas as pd
import requests
import os
from datetime import datetime
from config import DISCORD_WEBHOOK, ACTIVOS

def enviar_alerta(msg):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
    except:
        pass

def analizar_divergencias():
    fecha = datetime.now().strftime("%Y-%m-%d")
    base = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    
    try:
        # Cargar datos frescos
        spx = pd.read_csv(f"{base}/SPX/SPX_{fecha}_rt.csv").iloc[-1]
        spy = pd.read_csv(f"{base}/SPY/SPY_{fecha}_rt.csv").iloc[-1]
        vix = pd.read_csv(f"{base}/VIX/VIX_{fecha}_rt.csv").iloc[-1]
        ndx = pd.read_csv(f"{base}/NDX/NDX_{fecha}_rt.csv").iloc[-1]

        # Lógica de Inteligencia
        msg = f"🛰️ **INFORME SENTINEL - {datetime.now().strftime('%H:%M')}**\n"
        
        # 1. Alerta de VIX
        status_vix = "🔥 ALTA" if vix['spot'] > 20 else "🟢 NORMAL"
        msg += f"• **VIX:** {vix['spot']:.2f} ({status_vix})\n"
        
        # 2. Divergencia SPX vs SPY (Miedo)
        divergencia = spx['gex_total_vol'] - spy['gex_total_vol']
        msg += f"• **Divergencia SPX/SPY:** {divergencia:.2f} "
        msg += "⚠️ (MIEDO/COBERTURA)" if spy['gex_total_vol'] < -300 else "✅ OK"
        msg += "\n"
        
        # 3. Estado NDX (Tu "salto al vacío")
        msg += f"• **NDX Spot:** {ndx['spot']:.2f} | GEX: {ndx['gex_total_vol']:.2f}\n"
        
        enviar_alerta(msg)
    except Exception as e:
        # Si falla, no queremos que se rompa, solo que avise
        print(f"Error: {e}")

if __name__ == "__main__":
    analizar_divergencias()
