import json
import os
from datetime import datetime

def inject_data():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = "01_Backtesting_JSON"
    os.makedirs(folder, exist_ok=True)

    # Datos extraídos de tus imágenes de Research hoy
    research_data = {
        "SPY": {
            "ticker": "SPY",
            "date": today,
            "spot": 682.19,
            "put_wall": 680.00,
            "call_wall": 685.00,
            "vol_trigger": 680.00,
            "gamma_status": "Neutral"
        },
        "NDX": {
            "ticker": "NDX",
            "date": today,
            "spot": 24708.94,
            "put_wall": 24680.00,
            "call_wall": 24900.00,
            "vol_trigger": 24680.00,
            "gamma_status": "Neutral"
        }
    }

    for ticker, data in research_data.items():
        filename = f"{folder}/{ticker}_{today}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✅ Inyectado {ticker} en {filename}")

if __name__ == "__main__":
    inject_data()
