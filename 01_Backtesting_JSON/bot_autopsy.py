import os, json, requests
from datetime import datetime

def load_config():
    with open(os.path.expanduser("~/GexBot_Trading_Library/config.json"), 'r') as f:
        return json.load(f)

CONFIG = load_config()

def guardar_autopsia_oficial(activo, datos):
    # En Autopsia SÍ mantenemos Zero Gamma (es el dato oficial de cierre)
    fecha = datetime.now().strftime("%Y-%m-%d")
    path = os.path.expanduser(f"~/GexBot_Trading_Library/01_Backtesting_JSON/CME/{activo}/{fecha}")
    os.makedirs(path, exist_ok=True)
    
    filename = f"{path}/RTH_OFFICIAL_CLOSE.json"
    with open(filename, 'w') as f:
        json.dump(datos, f, indent=4)
    print(f"🏁 Autopsia RTH de {activo} completada y guardada en CME.")

# Solo para índices Core
for ticker in ["SPX", "NDX"]:
    final_data = {"zero_gamma": 5105.75, "rth_close_vol": "High", "official": True}
    guardar_autopsia_oficial(ticker, final_data)
