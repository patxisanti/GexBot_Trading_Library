import requests, sys, os, pytz, time
from datetime import datetime

sys.path.append(os.path.expanduser('~/GexBot_Trading_Library'))
try:
    from config import API_KEY, DISCORD_WEBHOOK, TIMEZONE_LOCAL, PAUSA_API
except:
    print("❌ Error: No se encuentra config.py")
    sys.exit(1)

# Sync con tu Futuro ES (Ajuste según ATAS)
FUTURES_OFFSET = 2.7 

def fetch_classic_zero(t):
    try:
        url = f"https://api.gexbot.com/{t.lower()}/classic/zero?key={API_KEY}"
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

def brain_alpha():
    tz = pytz.timezone(TIMEZONE_LOCAL)
    ts = datetime.now(tz).strftime("%H:%M")
    
    # Datos VIX para el contexto de riesgo
    vix_data = fetch_classic_zero("vix")
    vix_status = "⚪ ESTABLE"
    if vix_data:
        if (vix_data.get('spot') or 0) > (vix_data.get('zero_gamma') or 0):
            vix_status = "🔥 PELIGRO (VIX UP)"

    for t in ["SPX", "NDX"]:
        data = fetch_classic_zero(t)
        if not data: continue
        
        spot = (data.get('spot') or data.get('price', 0)) + FUTURES_OFFSET
        z0 = (data.get('zero_gamma') or 0) + FUTURES_OFFSET
        m_pos = (data.get('major_pos_vol') or 0) + FUTURES_OFFSET # Call Wall
        m_neg = (data.get('major_neg_vol') or 0) + FUTURES_OFFSET # Put Wall
        
        # --- LÓGICA DE PERFORACIÓN (WALL BREAKER) ---
        if spot < m_neg: 
            # Perforación Bajista
            bias_title, color, icon = "🚨 PÁNICO BAJISTA", 0x992d22, "💀"
            strat = f"🚨 **MURO PERFORADO (PUT WALL)**\n🔥 El precio ha roto los `{m_neg}`. Los Dealers están forzando la caída.\n⚠️ **NO BUSQUES REBOTES.** Es tendencia pura o Squeeze."
        elif spot > m_pos:
            # Perforación Alcista
            bias_title, color, icon = "🚨 EUFORIA ALCISTA", 0x1f8b4c, "🚀"
            strat = f"🚨 **MURO PERFORADO (CALL WALL)**\n🔥 El precio ha roto los `{m_pos}`. Short Squeeze activo.\n⚠️ **EL TECHO HA DESAPARECIDO.** Sigue la tendencia."
        elif spot < z0:
            # Zona Normal Bajista
            bias_title, color, icon = "SESGO BAJISTA", 0xe74c3c, "🔴"
            dist = round(spot - m_neg, 1)
            strat = f"🚀 **AIRPOCKET BAJISTA** hacia `{m_neg}` (Libre)" if dist > 15 else f"💎 **SOPORTE** en `{m_neg}`. Busca rebote de 5 pts."
        else:
            # Zona Normal Alcista
            bias_title, color, icon = "SESGO ALCISTA", 0x2ecc71, "🟢"
            dist = round(m_pos - spot, 1)
            strat = f"🚀 **AIRPOCKET ALCISTA** hacia `{m_pos}` (Libre)" if dist > 15 else f"💎 **RESISTENCIA** en `{m_pos}`. Busca reversión de 5 pts."

        payload = {"embeds": [{
            "title": f"🏛️ {t} | {icon} {bias_title}",
            "color": color,
            "description": f"{strat}\n\n🚥 **VIX:** `{vix_status}`",
            "fields": [
                {"name": "🚧 CALL WALL", "value": f"`{m_pos}`", "inline": True},
                {"name": "⚓ PUT WALL", "value": f"`{m_neg}`", "inline": True},
                {"name": "⚖️ ZERO GAMMA", "value": f"`{z0}`", "inline": True},
                {"name": "📊 PRECIO ES", "value": f"`{spot}`", "inline": True}
            ],
            "footer": {"text": f"v7.0 Wall-Breaker | {ts} | Sync Futuro"}
        }]}
        requests.post(DISCORD_WEBHOOK, json=payload)
        time.sleep(PAUSA_API)

if __name__ == "__main__":
    brain_alpha()
