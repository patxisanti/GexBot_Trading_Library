# -*- coding: utf-8 -*-
import pandas as pd
import os, requests
from datetime import datetime
from config import DISCORD_WEBHOOK

def analizar():
    f = datetime.now().strftime("%Y-%m-%d")
    path = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    
    try:
        # Carga de Sensores
        spx = pd.read_csv(f"{path}/SPX/SPX_{f}_rt.csv").iloc[-1]
        ndx = pd.read_csv(f"{path}/NDX/NDX_{f}_rt.csv").iloc[-1]
        spy = pd.read_csv(f"{path}/SPY/SPY_{f}_rt.csv").iloc[-1]
        vix = pd.read_csv(f"{path}/VIX/VIX_{f}_rt.csv").iloc[-1]

        # Lógica de Signos (Cian/Magenta)
        s_spx = spx['gex_total_vol'] > 0
        s_ndx = ndx['gex_total_vol'] > 0
        s_spy = spy['gex_total_vol'] > 0
        
        # Línea 2: SPX vs SPY
        div_spx_spy = "OK" if s_spx == s_spy else "⚠️ DIVERGENCIA"
        
        # Línea 3: NDX vs SPX
        es_sincro = s_ndx == s_spx
        div_ndx_spx = "OK (Sincronizados)" if es_sincro else "⚠️ Fracturado"
        fuerza = "NDX Lidera" if (s_ndx and ndx['gex_total_vol'] > 1000) else "SPX Lidera"

        # Construcción del Mensaje de 3 líneas (Formato solicitado)
        # Mantengo el número de Bot al inicio como pactamos
        msg = (f"**3 - DIVERGENCIA ÍNDICES (SPX/NDX)** - {datetime.now().strftime('%H:%M')}\n"
               f"• **VIX:** {vix['spot']:.2f} ({'NORMAL' if vix['spot'] < 20 else 'TENSO'})\n"
               f"• **Divergencia SPX/SPY:** {div_spx_spy} | **GEX SPX:** {spx['gex_total_vol']:.0f}\n"
               f"• **Divergencia NDX/SPX:** {div_ndx_spx} | **Fuerza:** {fuerza}")

        requests.post(DISCORD_WEBHOOK, json={"content": msg})
        print("Bot 03: Reporte 3-líneas enviado.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analizar()
