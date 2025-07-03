from bitvavo import Bitvavo
import streamlit as st

bitvavo = Bitvavo({
    'APIKEY': st.secrets["BITVAVO_API_KEY"],
    'APISECRET': st.secrets["BITVAVO_API_SECRET"],
    'RESTURL': 'https://api.bitvavo.com/v2',
    'WSURL': 'wss://ws.bitvavo.com/v2/'
})

def get_all_markets():
    markets = bitvavo.markets({})
    return [m['market'] for m in markets if m['quote'] == 'EUR']

def get_historical_candles(symbol, interval, limit=150):
    try:
        return bitvavo.candles(symbol, interval, {"limit": limit})
    except Exception as e:
        print(f"Fout bij candles ophalen: {e}")
        return []
