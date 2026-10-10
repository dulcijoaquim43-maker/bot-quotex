from flask import Flask
import threading
import time, requests, pandas as pd
from quotexapi.stable_api import Quotex

app = Flask(__name__)
@app.route('/')
def home():
    return "BOT LIGADO"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()

EMAIL = "dulcijoaquim43@gmail.com"
PASSWORD = "Djino141"
TELEGRAM_TOKEN = "8837469193:AAEJ70lhWK1qInSRO-QchA4i-yff9lSFRMY"
TELEGRAM_ID = "5523772563"

TODOS_PARES = ["EURUSD","GBPUSD","USDJPY","AUDUSD","EURGBP_otc","GBPUSD_otc","EURUSD_otc","GBPJPY_otc","USDJPY_otc","AUDUSD_otc","EURJPY_otc"]

q = Quotex(EMAIL, PASSWORD)
q.connect()

def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_ID, "text": msg, "parse_mode": "Markdown"})

def analisa_mesma_cor(df, qtd):
    cores = []
    for i in range(qtd):
        v = df.iloc[-(qtd+1)+i]
        corpo = abs(v['close'] - v['open'])
        total = v['high'] - v['low']
        if total == 0: return None
        pavio_contra = v['high'] - max(v['open'], v['close']) if v['close'] > v['open'] else min(v['open'], v['close']) - v['low']
        if corpo > total*0.60 and pavio_contra < total*0.35:
            cor = "verde" if v['close'] > v['open'] else "vermelha"
            cores.append(cor)
        else:
            return None
    if len(cores) == qtd and len(set(cores)) == 1:
        return cores[0]
    return None

while True:
    try:
        for par in TODOS_PARES:
            for timeframe in [60, 120]:
                tempo_str = "M1" if timeframe == 60 else "M2"
                velas = q.get_candles(par, timeframe, 100, time.time())
                df = pd.DataFrame(velas)
                df['EMA9'] = df['close'].ewm(span=9).mean()
                df['EMA20'] = df['close'].ewm(span=20).mean()
                df['EMA50'] = df['close'].ewm(span=50).mean()
                delta = df['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                df['RSI'] = 100 - (100 / (1 + gain/loss))
                atual = df.iloc[-1]
                cor6 = analisa_mesma_cor(df, 6)
                if cor6:
                    if cor6 == "verde":
                        ok = atual['close'] > atual['EMA9'] > atual['EMA20'] > atual['EMA50'] and 55 < atual['RSI'] < 75
                        direcao = "CALL 🟢"
                    else:
                        ok = atual['close'] < atual['EMA9'] < atual['EMA20'] < atual['EMA50'] and 25 < atual['RSI'] < 45
                        direcao = "PUT 🔴"
                    if ok:
                        enviar(f"🚀 SINAL {tempo_str} - {par} - 6 VELAS {cor6} - {direcao} - RSI {round(atual['RSI'],1)}")
                        time.sleep(50)
    except:
        time.sleep(5)
    time.sleep(3)
