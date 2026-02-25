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
    search_map = {"SPX": ["SPX", "SPY", "S&P"], "NDX": ["NDX", "QQQ", "NASDAQ"]}
    
    for ticker, aliases in search_map.items():
        found_file = None
        for alias in aliases:
            match = [f for f in os.listdir(folder) if alias in f and f.endswith(".json")]
            if match:
                found_file = max([os.path.join(folder, f) for f in match], key=os.path.getmtime)
                break
        
        if found_file:
            with open(found_file, 'r') as f:
                data = json.load(f)
            msg = f"🛡️ **SENTINEL VIVO [{ticker}]:**\n📍 Spot: **{data.get('spot')}**\n🧱 PW: **{data.get('put_wall')}** | 🏰 CW: **{data.get('call_wall')}**\n⚠️ Estado: *Vigilando fricción en niveles*"
            requests.post(webhook_url, json={"content": msg})
