from flask import Flask
import os
import threading
import time, requests, pandas as pd
from quotexapi.stable_api import Quotex

app = Flask(__name__)

@app.route('/')
def home():
    return "BOT LIGADO 24h ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Configurações - AGORA SEGURAS, pega do Render
EMAIL = os.environ.get("EMAIL", "")
PASSWORD = os.environ.get("PASSWORD", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_ID = os.environ.get("TELEGRAM_ID", "")

TODOS_PARES = ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD"]

def run_bot():
    print("Conectando Quotex...")
    q = Quotex(EMAIL, PASSWORD)
    q.connect()
    print("Bot Quotex iniciado!")
    while True:
        time.sleep(1)
        # aqui entra sua lógica do bot

# Inicia o Flask e o Bot juntos
threading.Thread(target=run_flask, daemon=True).start()

if __name__ == "__main__":
    run_bot()
