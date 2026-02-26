# --- 🔑 CLAVES DE ACCESO ---
API_KEY = "j0QzGW6qbPdG"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1474720425065054231/vBustmy6TNeRR33zCMxiIzRuqeTYOI6YY-Fqyf2lkxK_f_gCDI6m2DQ6VPB9EKuKKOHz"

# --- 🌍 COORDENADAS TEMPORALES (Canarias / Londres) ---
TIMEZONE_LOCAL = "Atlantic/Canary"    # Tu hora local
TIMEZONE_MARKET = "America/New_York"  # El origen de los datos

# --- ⏰ HORARIOS DE OPERACIÓN (Referencia NY) ---
# Los bots usarán esto para sincronizarse contigo en Canarias
NY_OPEN = "09:30"
NY_PRE_MARKET = "08:30"
NY_CLOSE = "16:00"

# --- 📊 LISTADO DE ACTIVOS (Tu Universo de Inversión) ---
INDICES = ["SPX", "NDX", "QQQ", "IWM"]
MAG7 = ["AAPL", "AMZN", "MSFT", "NVDA", "TSLA", "META", "GOOGL"]
RIESGO_BONOS = ["TLT", "HYG", "UVXY", "VIX"]
APALANCADOS = ["TQQQ", "SQQQ", "SPY"]

# Unión de todos los activos para el Recolector
ACTIVOS = INDICES + MAG7 + RIESGO_BONOS + APALANCADOS

# --- 🛡️ CONFIGURACIÓN DE SEGURIDAD ---
# Para no saturar la API (segundos entre peticiones)
PAUSA_API = 0.5
