import requests, os, sys
sys.path.append(os.path.expanduser('~/GexBot_Trading_Library'))
from config import API_KEY

def debug_ticker(ticker):
    url = f"https://api.gexbot.com/{ticker}/state/zero?key={API_KEY}"
    print(f"\n--- Probando {ticker} ---")
    try:
        r = requests.get(url)
        data = r.json()
        print(f"Status: {r.status_code}")
        print(f"Data recibida: {data}")
    except Exception as e:
        print(f"Error: {e}")

debug_ticker("SPX")
debug_ticker("SPY")
