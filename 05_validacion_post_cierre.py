# -*- coding: utf-8 -*-
import pandas as pd
import os, requests, csv
from datetime import datetime
from config import DISCORD_WEBHOOK

def guardar_memoria(datos):
    log_file = "/root/GexBot_Trading_Library/auditoria_historica.csv"
    file_exists = os.path.isfile(log_file)
    with open(log_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=datos.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(datos)

def analizar():
    f = datetime.now().strftime("%Y-%m-%d")
    path = "/root/GexBot_Trading_Library/01_Backtesting_JSON"
    archivo_spx = f"{path}/SPX/SPX_{f}_rt.csv"
    archivo_ndx = f"{path}/NDX/NDX_{f}_rt.csv"

    try:
        if not os.path.exists(archivo_spx):
            print("Esperando datos de cierre...")
            return

        df_spx = pd.read_csv(archivo_spx)
        df_ndx = pd.read_csv(archivo_ndx)
        ini_spx, fin_spx = df_spx.iloc[0], df_spx.iloc[-1]
        ini_ndx, fin_ndx = df_ndx.iloc[0], df_ndx.iloc[-1]

        # 1. AUDITORÍA BOT 01 (Sesgo de Apertura)
        # ¿El bando inicial predijo la dirección final?
        exito_01 = (ini_spx['gex_total_vol'] > 0 and fin_spx['spot'] > ini_spx['spot']) or \
                   (ini_spx['gex_total_vol'] < 0 and fin_spx['spot'] < ini_spx['spot'])
        
        # 2. AUDITORÍA BOT 03 (Liderazgo)
        perf_spx = (fin_spx['spot'] - ini_spx['spot']) / ini_spx['spot']
        perf_ndx = (fin_ndx['spot'] - ini_ndx['spot']) / ini_ndx['spot']
        # ¿El que tenía más GEX relativo lideró el rendimiento?
        exito_03 = (perf_ndx > perf_spx if ini_ndx['gex_total_vol'] > ini_spx['gex_total_vol'] else perf_spx > perf_ndx)

        # 3. DINÁMICA DE LIQUIDEZ (GEX Accretion/Leakage)
        delta_gex = fin_spx['gex_total_vol'] - ini_spx['gex_total_vol']
        calidad_rally = "ACUMULACIÓN ✅" if delta_gex > 0 else "DISTRIBUCIÓN (Squeeze) ⚠️"

        # 4. GUARDAR EN MEMORIA (Caja Negra)
        datos_auditoria = {
            "fecha": f,
            "spx_perf": round(perf_spx * 100, 2),
            "ndx_perf": round(perf_ndx * 100, 2),
            "bot01_hit": 1 if exito_01 else 0,
            "bot03_hit": 1 if exito_03 else 0,
            "delta_gex_total": round(delta_gex, 0)
        }
        guardar_memoria(datos_auditoria)

        # 5. INFORME PARA EL COMANDANTE
        msg = (f"**5 - MAESTRO DE AUDITORÍA**\n"
               f"--- Balance de Sesión: {f} ---\n"
               f"• **Bot 01 (Escenarios):** {'ACERTADO ✅' if exito_01 else 'FALLIDO ❌'}\n"
               f"• **Bot 03 (Liderazgo):** {'CONFIRMADO ✅' if exito_03 else 'RUIDO ⚠️'}\n"
               f"• **Flujo Institucional:** {calidad_rally}\n"
               f"• **Rendimientos:** SPX: {perf_spx*100:+.2f}% | NDX: {perf_ndx*100:+.2f}%\n"
               f"• **GEX Delta:** {delta_gex:+.0f} pts (Liquidez {'añadida' if delta_gex > 0 else 'retirada'})\n"
               f"--- *Resultado guardado en historial para aprendizaje del sistema.* ---")

        requests.post(DISCORD_WEBHOOK, json={"content": msg})
        print("Bot 05: Auditoría completada y memoria guardada.")

    except Exception as e:
        print(f"Error en el Maestro: {e}")

if __name__ == "__main__":
    analizar()
