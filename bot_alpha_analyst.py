# -*- coding: utf-8 -*-
import pandas as pd
import os
import requests
from datetime import datetime
from config import DISCORD_WEBHOOK

def enviar_discord(titulo, color, descripcion, campos):
    payload = {
        "embeds": [{
            "title": titulo,
            "color": color,
            "description": descripcion,
            "fields": campos,
            "footer": {"text": f"Sentinel Scout v2.5 | {datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

def analizar_divergencias():
    f = datetime.now().strftime("%Y-%m-%d")
    path = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    
    try:
        # 1. Carga de Sensores Disponibles
        spx = pd.read_csv(f"{path}/SPX/SPX_{f}_rt.csv").iloc[-1]
        ndx = pd.read_csv(f"{path}/NDX/NDX_{f}_rt.csv").iloc[-1]
        spy = pd.read_csv(f"{path}/SPY/SPY_{f}_rt.csv").iloc[-1]
        vix = pd.read_csv(f"{path}/VIX/VIX_{f}_rt.csv").iloc[-1]

        alertas = []
        
        # --- LÓGICA DE DEBILIDAD Y CUBRIMIENTO ---
        
        # A. Debilidad Tech (NDX vs SPX)
        if ndx['gex_total_vol'] < 0 and spx['gex_total_vol'] > 0:
            alertas.append("⚠️ **DEBILIDAD NDX**: El sector Tech está en territorio de ventas (GEX Negativo) mientras el SPX intenta aguantar. Riesgo de arrastre.")

        # B. Cubrimiento Masivo (SPY vs SPX)
        # El SPY suele reflejar el miedo del retail/institucional pequeño
        if spy['gex_total_vol'] < -300:
            alertas.append("🚨 **CUBRIMIENTO MASIVO SPY**: Hay una muralla de Puts en el ETF. Los dealers están forzados a vender si el precio baja.")

        # C. Zona de Resbalón (Zero Gamma)
        dist_zero = spx['spot'] - spx['zero_gamma']
        if abs(dist_zero) < 10:
            alertas.append("🎢 **PUNTO DE INFLEXIÓN**: SPX está sobre el Zero Gamma. Espera volatilidad violenta; el mercado no tiene dirección clara aquí.")

        # 2. Envío a Discord si hay algo interesante
        if alertas:
            campos = [
                {"name": "VIX", "value": f"{vix['spot']:.2f}", "inline": True},
                {"name": "SPX Spot", "value": f"{spx['spot']:.2f}", "inline": True},
                {"name": "GEX Total", "value": f"{spx['gex_total_vol']:.0f}", "inline": True}
            ]
            enviar_discord("🛰️ REPORTE DE DIVERGENCIAS Y FRAGILIDAD", 15105570, "\n\n".join(alertas), campos)
            
    except Exception as e:
        print(f"Esperando a que todos los CSV tengan datos... ({e})")

if __name__ == "__main__":
    analizar_divergencias()
