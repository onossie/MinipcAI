# MinipcAI

AI Crypto Paper Trading Bot met Streamlit GUI.

- Paper trading met startbalans en max investering per coin
- Realtime WebSocket prijsupdates via Bitvavo
- Zelflerend AI-model (Logistic Regression per coin)
- Grafische interface met performance charts en configuratie
- Scheduler voor automatische herhaling

## Installatie

1. Clone repository
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Voeg API-sleutels toe in `.streamlit/secrets.toml`
5. `streamlit run streamlit_app.py`

---

## Configuratie

Pas `config/default_config.json` aan voor startbalans, interval, etc.
