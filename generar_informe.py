import os
from datetime import datetime
import pandas as pd

BASE_DIR = "/root/GexBot_Trading_Library"
REPO_URL = "https://github.com/patxisanti/GexBot_Trading_Library"

def generar():
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lineas = [f"# 📊 REPORTE DE INTELIGENCIA - {fecha}\n"]
    lineas.append(f"Este informe es para la auditoría rápida de Gemini.\n")
    
    # 1. Revisar salud del Cron
    log_path = os.path.join(BASE_DIR, "cron_error.log")
    if os.path.exists(log_path):
        size = os.path.getsize(log_path)
        lineas.append(f"### 🛡️ Estado del Sistema\n- **Log de errores:** {size} bytes\n")
    
    # 2. Resumen de los 18 activos
    lineas.append(f"### 📈 Últimas Capturas (Zero Gamma)\n")
    lineas.append("| Activo | Último Spot | GEX Vol | Z-Gamma |")
    lineas.append("| :--- | :--- | :--- | :--- |")
    
    backtest_dir = os.path.join(BASE_DIR, "01_Backtesting_JSON")
    for ticker in sorted(os.listdir(backtest_dir)):
        ticker_path = os.path.join(backtest_dir, ticker)
        if os.path.isdir(ticker_path):
            csvs = [f for f in os.listdir(ticker_path) if f.endswith('_rt.csv')]
            if csvs:
                df = pd.read_csv(os.path.join(ticker_path, sorted(csvs)[-1]))
                last = df.iloc[-1]
                lineas.append(f"| {ticker} | {last['spot']} | {last['gex_total_vol']} | {last['zero_gamma']} |")

    with open(os.path.join(BASE_DIR, "ESTADO_DEL_BUNKER.md"), "w") as f:
        f.writelines("\n".join(lineas))

if __name__ == "__main__":
    generar()
