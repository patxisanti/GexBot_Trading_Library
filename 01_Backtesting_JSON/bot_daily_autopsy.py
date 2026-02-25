import json
import os
import requests
from datetime import datetime

def load_config():
    config_path = os.path.expanduser("~/GexBot_Trading_Library/config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    config = load_config()
    if not config:
        print("❌ Error: config.json no encontrado")
        return

    webhook_url = config.get("discord_webhook")
    today = datetime.now().strftime("%Y-%m-%d")
    
    report_header = f"📋 **AUTOPSIA DIARIA SENTINEL: {today}**\n"
    summary = ""

    for ticker in ["SPX", "NDX"]:
        file_path = os.path.expanduser(f"~/GexBot_Trading_Library/01_Backtesting_JSON/{ticker}_{today}.json")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            summary += f"\n**{ticker}:**\n"
            summary += f"- Cierre Spot: {data.get('spot')}\n"
            summary += f"- Rango del día: {data.get('put_wall')} (PW) a {data.get('call_wall')} (CW)\n"
        else:
            summary += f"\n⚠️ Datos de {ticker} no disponibles para autopsia."

    # Enviar a Discord
    requests.post(webhook_url, json={"content": report_header + summary})
    
    # Guardar informe físico en la carpeta 02_Informes_Texto
    log_path = os.path.expanduser(f"~/GexBot_Trading_Library/02_Informes_Texto/Autopsia_{today}.txt")
    with open(log_path, 'w') as f:
        f.write(report_header + summary)
    
    print(f"✅ Autopsia generada y enviada.")

if __name__ == "__main__":
    main()
