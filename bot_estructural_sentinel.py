# -*- coding: utf-8 -*-
import pandas as pd
import os
import requests
from datetime import datetime
from config import DISCORD_WEBHOOK

# ==========================================
# CONFIGURACIÓN CRÍTICA JPM COLLAR Q1 2026
# ==========================================
CADUCIDAD_COLLAR = datetime(2026, 3, 31)

NIVELES_Q = {
    'CALL': 7000.00,      # Techo Institucional
    'PUT_H': 6330.00,     # Put Wall (Suelo de Cobertura)
    'PUT_B': 5340.00      # Suelo del Pánico
}
# ==========================================

def enviar_alerta_roja(msg):
    requests.post(DISCORD_WEBHOOK, json={"content": f"🔴 **ALERTA CADUCIDAD**: {msg}"})

def analizar_estructural():
    ahora = datetime.now()

    if ahora > CADUCIDAD_COLLAR:
        enviar_alerta_roja(f"Niveles JPM caducados el {CADUCIDAD_COLLAR.strftime('%Y-%m-%d')}.")
        return

    fecha_hoy = ahora.strftime("%Y-%m-%d")
    ruta_spx = f"/root/GexBot_Trading_Library/01_Backtesting_JSON/SPX/SPX_{fecha_hoy}_rt.csv"

    if not os.path.exists(ruta_spx): return

    try:
        df = pd.read_csv(ruta_spx)
        last = df.iloc[-1]
        spot = last['spot']
        
        dist_call = NIVELES_Q['CALL'] - spot
        dist_put = spot - NIVELES_Q['PUT_H']

        # Determinamos en qué zona del rango estamos
        rango_total = NIVELES_Q['CALL'] - NIVELES_Q['PUT_H']
        posicion_relativa = ((spot - NIVELES_Q['PUT_H']) / rango_total) * 100

        payload = {
            "embeds": [{
                "title": "🏛️ Sentinel Estructural - Mapa de Rango",
                "color": 65280,
                "description": f"✅ **Vigencia:** Q1 2026 (Exp: {CADUCIDAD_COLLAR.strftime('%Y-%m-%d')})",
                "fields": [
                    {"name": "Spot Actual", "value": f"**{spot:.2f}**", "inline": False},
                    {"name": "📈 Call Wall (Techo)", "value": f"{NIVELES_Q['CALL']:.2f}\n*(A {dist_call:.2f} pts)*", "inline": True},
                    {"name": "📉 Put Wall (Suelo)", "value": f"{NIVELES_Q['PUT_H']:.2f}\n*(A {dist_put:.2f} pts)*", "inline": True},
                    {"name": "📍 Posición en Rango", "value": f"Estamos al **{posicion_relativa:.1f}%** del suelo institucional.", "inline": False}
                ],
                "footer": {"text": "Bot #2 - Inteligencia de Capas Tectónicas"}
            }]
        }
        requests.post(DISCORD_WEBHOOK, json=payload)

    except Exception as e:
        enviar_alerta_roja(f"Error técnico: {str(e)}")

if __name__ == "__main__":
    analizar_estructural()
