import requests
import json
import os
from datetime import datetime

def load_config():
    config_path = os.path.expanduser("~/GexBot_Trading_Library/config.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_plan(ticker, data):
    spot, pw, cw = data.get("spot"), data.get("put_wall"), data.get("call_wall")
    # Para el SPX y NDX, el margen de proximidad es mayor (aprox 5-10 puntos)
    dist = abs(spot - pw)
    
    plan = f"📊 **PLAN INSTITUCIONAL: {ticker}**\n📍 SPOT: {spot} | 🧱 PUT WALL: {pw} | 🏰 CALL WALL: {cw}\n\n"
    
    if spot > pw and dist < 10:
        plan += "🔥 **ESCENARIO: REBOTE EN MURO (VANNA).**\nEl precio está acariciando el Put Wall. Si el Orderflow confirma, buscamos giro al alza."
    elif spot < pw:
        plan += "⚠️ **ALERTA: GAMMA NEGATIVA (CASCADA).**\nEstamos por debajo del soporte principal. Peligro de aceleración."
    else:
        plan += "⚖️ **ESCENARIO: DERIVA (CHOPPY).**\nEl precio tiene aire hasta los muros. Operar con cautela."
    return plan

def main():
    config = load_config()
    webhook = config.get("discord_webhook")
    
    # Datos proyectados para SPX y NDX (Ajustados a escala de Índice)
    research_today = {
        "SPX": {"spot": 6821.9, "put_wall": 6800.0, "call_wall": 6850.0},
        "NDX": {"spot": 24708.9, "put_wall": 24680.0, "call_wall": 24900.0}
    }

    for ticker, data in research_today.items():
        plan_msg = generate_plan(ticker, data)
        requests.post(webhook, json={"content": plan_msg})

if __name__ == "__main__":
    main()
