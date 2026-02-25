import json
import os
import requests
from datetime import datetime

def load_config():
    config_path = os.path.expanduser("~/GexBot_Trading_Library/config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return None

def main():
    config = load_config()
    if not config: return
    webhook_url = config.get("discord_webhook")
    folder = os.path.expanduser("~/GexBot_Trading_Library/01_Backtesting_JSON/")
    
    # El Health Scout busca anomalías en los archivos más recientes
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json")]
    if not files: return
    
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Lógica de ballenas: Detectamos si el Spot se acerca peligrosamente a un muro
    distancia_pw = abs(data.get('spot', 0) - data.get('put_wall', 0))
    if distancia_pw < 15:
        msg = f"🐳 **HEALTH SCOUT - ALERTA DE BALLENAS:**\n⚠️ El precio está a {distancia_pw:.2f} puntos del **PUT WALL**.\n🔥 Posible defensa institucional en marcha."
        requests.post(webhook_url, json={"content": msg})
