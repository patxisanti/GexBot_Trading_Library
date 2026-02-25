import pandas as pd
import os
from datetime import datetime

# Configuración de niveles desde tu captura de pantalla (puedes actualizarlos)
NIVELES = {
    'SPX': {'Cian': 6942.50, 'Purpura': 6880.00, 'Zero': 6939.00},
    'NDX': {'Cian': 25371.00, 'Purpura': 25200.00, 'Zero': 25221.00}
}

def monitor():
    fecha = datetime.now().strftime("%Y-%m-%d")
    print(f"\n--- 🛰️  SENTINEL HUD - {datetime.now().strftime('%H:%M:%S')} ---")
    
    for ticker in ['SPX', 'NDX', 'SPY']:
        ruta = f"/root/GexBot_Trading_Library/01_Backtesting_JSON/{ticker}/{ticker}_{fecha}_rt.csv"
        if os.path.exists(ruta):
            df = pd.read_csv(ruta)
            last = df.iloc[-1]
            spot = last['spot']
            gex = last['gex_total_vol']
            
            # Cálculo de distancias si el nivel existe
            dist_info = ""
            if ticker in NIVELES:
                cian = NIVELES[ticker]['Cian']
                dist = cian - spot
                dist_info = f" | Dist a Cian: {dist:.2f}"
            
            emoji = "🟢" if gex > 0 else "🔴"
            print(f"{emoji} {ticker:<4} | Spot: {spot:<8} | GEX: {gex:<8.2f}{dist_info}")

if __name__ == "__main__":
    monitor()
