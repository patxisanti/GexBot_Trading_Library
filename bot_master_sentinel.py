# -*- coding: utf-8 -*-
import pandas as pd
import os
import requests
from datetime import datetime
from config import DISCORD_WEBHOOK
from sentinel_narrative import obtener_narrativa

def enviar_a_discord(ticker, spot, gex, escenario_id, extra_info=""):
    esc = obtener_narrativa(escenario_id)
    payload = {
        "embeds": [{
            "title": f"{esc['i']} {esc['t']} - {ticker}",
            "color": int(esc['col'].replace("#", ""), 16),
            "description": f"**Análisis:** {esc['c']}\n**Dato Extra:** {extra_info}",
            "fields": [
                {"name": "Spot", "value": f"{spot:.2f}", "inline": True},
                {"name": "GEX Vol", "value": f"{gex:.2f}", "inline": True},
                {"name": "Estrategia", "value": f"`{esc['tr']}`", "inline": True}
            ],
            "footer": {"text": f"Sentinel Alpha v2.4 | {datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

def analizar_mercado():
    fecha = datetime.now().strftime("%Y-%m-%d")
    base_path = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    
    try:
        spx = pd.read_csv(f"{base_path}/SPX/SPX_{fecha}_rt.csv").iloc[-1]
        ndx = pd.read_csv(f"{base_path}/NDX/NDX_{fecha}_rt.csv").iloc[-1]
        vix = pd.read_csv(f"{base_path}/VIX/VIX_{fecha}_rt.csv").iloc[-1]

        # --- CORRECCIÓN DE LÓGICA DE DIVERGENCIAS ---
        # Solo hay divergencia real si los bandos (Gamma + o -) son distintos
        if ndx['gex_total_vol'] < 0 and spx['gex_total_vol'] > 0:
            div_msg = "⚠️ NDX en Short Gamma (Peligro) vs SPX en Long Gamma"
            id_esc_ndx = "Z_DIV_H"
        elif ndx['gex_total_vol'] > 0 and spx['gex_total_vol'] < 0:
            div_msg = "🚀 NDX Liderando (Cian) vs SPX en Short Gamma"
            id_esc_ndx = "C_AIR_A2"
        else:
            div_msg = "✅ Confluencia de mercado"
            # Si ambos son positivos, usamos escenario de momentum cian
            id_esc_ndx = "C_AIR_A2" if ndx['gex_total_vol'] > 0 else "Z_FLIP_C"

        # Escenario SPX
        id_esc_spx = "C_AIR_A2" if spx['gex_total_vol'] > 0 else "M_AIR_A3"
        
        vix_status = "🟢 VIX Tranquilo" if vix['spot'] < 20 else "🔥 VIX Tenso"

        # Enviar reportes
        enviar_a_discord("SPX", spx['spot'], spx['gex_total_vol'], id_esc_spx, f"{vix_status} | {div_msg}")
        
        # Solo enviamos el NDX si hay algo que destacar o si quieres el reporte dual
        if div_msg != "✅ Confluencia de mercado":
            enviar_a_discord("NDX", ndx['spot'], ndx['gex_total_vol'], id_esc_ndx, div_msg)

    except Exception as e:
        print(f"Sincronizando sensores... {e}")

if __name__ == "__main__":
    analizar_mercado()
