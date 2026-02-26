# -*- coding: utf-8 -*-
import pandas as pd
import os, requests
from datetime import datetime
from config import DISCORD_WEBHOOK

def obtener_intensidad(valor):
    abs_v = abs(valor)
    if abs_v < 250: return "Baja"
    if abs_v < 1000: return "Media"
    return "Alta"

def obtener_semaforo(valor):
    if valor > 100: return "🟢"  # Positivo sólido
    if valor < -100: return "🔴" # Negativo sólido
    return "🟡"                # Neutral / Zona de Flip

def analizar():
    f = datetime.now().strftime("%Y-%m-%d")
    path = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    mag7 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    puntos = 0
    detalles = []

    for t in mag7:
        try:
            archivo = f"{path}/{t}/{t}_{f}_rt.csv"
            df = pd.read_csv(archivo)
            if df.empty: continue
            
            actual = df.iloc[-1]
            inicial = df.iloc[0]
            
            # 1. Variación de Precio
            pct = ((actual['spot'] - inicial['spot']) / inicial['spot']) * 100
            
            # 2. Análisis del Bando y Semáforo
            gex = actual['gex_total_vol']
            semaforo = obtener_semaforo(gex)
            intensidad = obtener_intensidad(gex)
            
            # Texto descriptivo del bando
            if gex > 100:
                bando = "Positivo (+)"
                puntos += 1
            elif gex < -100:
                bando = "Negativo (-)"
            else:
                bando = "Neutral (±)"
            
            # 3. Formato solicitado: Precio | Bando | Fuerza + Semáforo
            detalles.append(f"**{t}**: {pct:+.2f}% | {bando} | Fuerza: {intensidad} {semaforo}")
            
        except:
            continue

    if detalles:
        estado = "MERCADO SALUDABLE ✅" if puntos >= 5 else "MERCADO FRÁGIL ⚠️"
        
        msg = (f"**4 - SALUD MAG7**\n"
               f"--- {datetime.now().strftime('%H:%M')} ---\n"
               f"• **Diagnóstico:** {estado} ({puntos}/7)\n"
               f"--- Análisis Cualitativo ---\n"
               + "\n".join(detalles))
        
        requests.post(DISCORD_WEBHOOK, json={"content": msg})

if __name__ == "__main__":
    analizar()
