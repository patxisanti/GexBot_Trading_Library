# -*- coding: utf-8 -*-
import os, json, requests, sys
from datetime import datetime
import pytz

sys.path.append(os.path.expanduser("~/GexBot_Trading_Library"))

def load_config():
    with open(os.path.expanduser("~/GexBot_Trading_Library/config.json"), 'r') as f:
        return json.load(f)

CONFIG = load_config()

def enviar_discord_flow(ticker, alert_type, level, intensity):
    """Envía alertas de Fricción o Velocidad (Pilar 4 y 5)"""
    webhook = CONFIG.get("discord_webhook")
    if not webhook: return

    # Colores: Cian para absorción/fricción, Magenta para aceleración
    color = 65535 if "FRICCIÓN" in alert_type else 16711935
    icono = "🧱" if "FRICCIÓN" in alert_type else "⚡"
    
    payload = {
        "embeds": [{
            "title": f"{icono} {alert_type}: {ticker}",
            "color": color,
            "fields": [
                {"name": "📍 Nivel State", "value": f"`{level}`", "inline": True},
                {"name": "📊 Intensidad", "value": f"`{intensity}`", "inline": True},
                {"name": "💡 Fontanería", "value": "Detectado desbalance en el Tape. El Dealer está absorbiendo flujo masivo aquí." if "FRICCIÓN" in alert_type else "Vía libre detectada. El flujo atraviesa el nivel sin resistencia.", "inline": False}
            ],
            "footer": {"text": "Sentinel Orderflow - Vigilancia de Fricción"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try: requests.post(webhook, json=payload, timeout=5)
    except: print("⚠️ Error en Discord Flow")

def fetch_flow_data(ticker):
    # Simulación de detección de Spikes (En prod: lectura de cinta/API Flow)
    try:
        url = f"https://www.gexbot.com/api/v1/state/{ticker}" # Usamos state como base
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

def main():
    tz_ny = pytz.timezone('America/New_York')
    ny_now = datetime.now(tz_ny)
    h_ny = ny_now.strftime("%H:%M")

    # PILAR AMBRUS: No procesar antes de las 09:33 NY
    if h_ny < "09:33":
        return

    for ticker in CONFIG.get("active_tickers", ["SPX"]):
        data = fetch_flow_data(ticker)
        if not data: continue
        
        # LÓGICA DE DETECCIÓN (Pilares 4 y 9)
        # Si el volumen relativo es muy alto en un muro -> FRICCIÓN (Cyan Spike)
        vol_rel = data.get('volume', 0) / data.get('avg_volume', 1)
        
        if vol_rel > 2.0:
            enviar_discord_flow(ticker, "FRICCIÓN DETECTADA (Cyan Spike)", data.get('put_wall'), "CRÍTICA")
        elif vol_rel > 1.5:
            enviar_discord_flow(ticker, "VELOCIDAD DE FLUJO (Air Pocket)", "N/A", "ALTA")

if __name__ == "__main__":
    main()
