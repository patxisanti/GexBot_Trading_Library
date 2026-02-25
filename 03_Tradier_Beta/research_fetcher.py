import requests
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
# Basado en la documentación de gexbot.com/docs
API_BASE_URL = "https://api.gexbot.com/v2" # Ajustar según tu config.json
API_KEY = "TU_API_KEY_AQUI"
DISCORD_WEBHOOK = "TU_WEBHOOK_AQUI"
TICKERS = ["SPY", "NDX"]

def fetch_gex_research(ticker):
    print(f"[{datetime.now()}] Extrayendo Research para {ticker}...")
    endpoint = f"{API_BASE_URL}/research/{ticker}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Error {response.status_code} en {ticker}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def save_and_alert(ticker, data):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = "GexBot_Trading_Library/01_Backtesting_JSON"
    filename = f"{folder}/{ticker}_{today}.json"
    
    # Extraer niveles clave (Métrica de los 12 Pilares)
    put_wall = data.get("put_wall")
    call_wall = data.get("call_wall")
    vol_trigger = data.get("vol_trigger")
    
    # Guardar JSON
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Notificar a Discord (Para tu tranquilidad mental)
    msg = (f"🎯 **SENTINEL ALPHA: Research Cargado ({ticker})**\n"
           f"🧱 **Put Wall:** {put_wall}\n"
           f"🏰 **Call Wall:** {call_wall}\n"
           f"⚡ **Vol Trigger:** {vol_trigger}\n"
           f"📂 Guardado en: `{filename}`")
    
    requests.post(DISCORD_WEBHOOK, json={"content": msg})

if __name__ == "__main__":
    for ticker in TICKERS:
        data = fetch_gex_research(ticker)
        if data:
            save_and_alert(ticker, data)
