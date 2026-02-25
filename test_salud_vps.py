import sys
import os
import requests
import subprocess
import datetime

# IMPORTACIÓN AUTOMÁTICA DE CLAVES (Sin meterlas a mano)
sys.path.append(os.path.expanduser('~/GexBot_Trading_Library'))
from config import API_KEY, DISCORD_WEBHOOK

def check_disk():
    # Verifica el espacio en la partición principal
    st = os.statvfs('/')
    free_gb = (st.f_bavail * st.f_frsize) / (1024**3)
    return round(free_gb, 2)

def check_latency(host):
    cmd = f"ping -c 4 {host} | tail -1 | awk '{{print $4}}' | cut -d '/' -f 2"
    return float(subprocess.check_output(cmd, shell=True).decode().strip())

# Ejecución
lat = check_latency("api.gexbot.com")
disco = check_disk()
status = "🟢" if lat < 30 and disco > 5 else "🟡" if lat < 70 else "🔴"

msg = {
    "content": (f"🛡️ **REPORTE ALPHA DE INFRAESTRUCTURA**\n"
                f"📡 Latencia Gexbot: `{lat} ms`\n"
                f"💾 Espacio Libre: `{disco} GB`\n"
                f"📊 Estado General: **{status}**\n"
                f"📅 Verificado: `{datetime.datetime.now().strftime('%H:%M:%S')}`")
}

requests.post(DISCORD_WEBHOOK, json=msg)

