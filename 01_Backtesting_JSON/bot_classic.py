# -*- coding: utf-8 -*-
import os, json, requests
from datetime import datetime

def load_config():
    with open(os.path.expanduser("~/GexBot_Trading_Library/config.json"), 'r') as f:
        return json.load(f)

CONFIG = load_config()

def enviar_discord_niveles(ticker, data):
    webhook = CONFIG.get("discord_webhook")
    if not webhook: return
    
    payload = {
        "embeds": [{
            "title": f"📐 MAPA ESTRUCTURAL: {ticker}",
            "color": 3447003, # Azul
            "fields": [
                {"name": "🚀 LONG CONVEXITY (TECHO)", "value": f"`{data.get('call_wall', 'N/A')}`", "inline": True},
                {"name": "📉 SHORT CONVEXITY (SUELO)", "value": f"`{data.get('put_wall', 'N/A')}`", "inline": True},
                {"name": "⚖️ ZERO GAMMA", "value": f"`{data.get('zero_gamma', 'N/A')}`", "inline": True}
            ],
            "footer": {"text": "Niveles Classic - Muros de Cemento"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    requests.post(webhook, json=payload, timeout=5)

def main():
    # Solo procesamos SPX y NDX para no saturar Discord
    for ticker in ["SPX", "NDX"]:
        try:
            r = requests.get(f"https://www.gexbot.com/api/v1/state/{ticker}", timeout=10)
            if r.status_code == 200:
                enviar_discord_niveles(ticker, r.json())
        except: pass

if __name__ == "__main__":
    main()
