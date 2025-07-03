import streamlit as st
import json
import time
import threading
import matplotlib.pyplot as plt
from datetime import datetime
from bitvavo.bitvavo_interface import get_all_markets, get_historical_candles
from ai.model_logic import train_model, predict_trade
from trading.paper_trader import PaperTrader
from utils.logger import setup_logger
import schedule

setup_logger()

st.set_page_config(page_title="MinipcAI Bot", layout="wide")
st.title("🤖 MinipcAI - Paper Trading Bot")

# Load config
with open("config/default_config.json") as f:
    config = json.load(f)

# Sidebar configuratie
st.sidebar.header("🔧 Configuratie")
start_balance = st.sidebar.number_input("Start balans (€)", value=config["start_balance"])
max_per_coin = st.sidebar.number_input("Max investering per coin (€)", value=config["max_invest_per_coin"])
min_history = config["min_candle_history"]
interval = config["interval"]
scheduler_minutes = config.get("scheduler_interval_minutes", 15)

if "trader" not in st.session_state:
    st.session_state["trader"] = None
if "running" not in st.session_state:
    st.session_state["running"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []
if "net_values" not in st.session_state:
    st.session_state["net_values"] = []
if "progress" not in st.session_state:
    st.session_state["progress"] = {}

def run_bot():
    st.session_state["running"] = True
    trader = PaperTrader(start_balance)
    st.session_state["trader"] = trader

    symbols = get_all_markets()
    total_symbols = len(symbols)
    progress_bar = st.progress(0)
    status_text = st.empty()

    prices_snapshot = {}

    for idx, symbol in enumerate(symbols):
        status_text.text(f"Processing {symbol} ({idx+1}/{total_symbols})")

        candles = get_historical_candles(symbol, interval, limit=min_history)
        if len(candles) < min_history:
            status_text.text(f"Skipping {symbol}: onvoldoende candles")
            continue

        model = train_model(candles)
        decision = predict_trade(model, candles)
        current_price = float(candles[-1][2])

        if decision == 1:
            amount = round(max_per_coin / current_price, 5)
            trader.buy(symbol, current_price, amount)
        else:
            if trader.holdings[symbol] > 0:
                trader.sell(symbol, current_price, trader.holdings[symbol])

        prices_snapshot[symbol] = current_price
        st.session_state["progress"][symbol] = trader.holdings[symbol]

        progress_bar.progress((idx + 1) / total_symbols)

    net_val = trader.net_value(prices_snapshot)
    st.session_state["net_values"].append(net_val)
    st.session_state["history"].extend(trader.history)
    st.session_state["running"] = False
    status_text.text("Bot run voltooid!")

def background_scheduler():
    schedule.every(scheduler_minutes).minutes.do(run_bot)
    while True:
        schedule.run_pending()
        time.sleep(10)

if st.sidebar.button("Start Bot"):
    if not st.session_state["running"]:
        threading.Thread(target=run_bot, daemon=True).start()
    else:
        st.warning("Bot is al aan het draaien!")

st.sidebar.write(f"Scheduler draait elke {scheduler_minutes} minuten automatisch.")

if st.sidebar.button("Start Scheduler"):
    threading.Thread(target=background_scheduler, daemon=True).start()
    st.sidebar.success("Scheduler gestart!")

st.subheader("📈 Winstgrafiek")
if st.session_state["net_values"]:
    plt.figure(figsize=(10, 4))
    plt.plot(st.session_state["net_values"], label="Netto waarde (€)")
    plt.xlabel("Run #")
    plt.ylabel("Waarde (€)")
    plt.legend()
    st.pyplot(plt)

st.subheader("📝 Transactiegeschiedenis")
if st.session_state["history"]:
    for action, coin, price, amount in reversed(st.session_state["history"][-50:]):
        st.write(f"{action} {amount:.5f} {coin} @ €{price:.4f}")

st.subheader("🔍 Huidige holdings")
if st.session_state["trader"]:
    holdings = st.session_state["trader"].holdings
    for coin, amount in holdings.items():
        st.write(f"{coin}: {amount:.5f}")
