import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os
from data_manager import load_trades, save_trades, add_trade

# This block helps me move my file without having to change names each time.
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

TRADES_FILE = get_data_path("trades.csv")

st.title("Portfolio Manager")
st.write("Trade journal and performance dashboard.")
st.write("Trades file path:", TRADES_FILE)

trades_df = load_trades(TRADES_FILE)
st.subheader("Saved Trades")
st.dataframe(trades_df)

st.subheader("Add a New Trade")

with st.form("add_trade_form"):
    ticker = st.text_input("Ticker Symbol", placeholder="AAPL")
    buy_price = st.number_input("Buy Price", min_value=0.0, step=0.01)
    buy_date = st.date_input("Buy Date")

    sell_price = st.number_input("Sell Price", min_value=0.0, step=0.01)
    sell_date = st.date_input("Sell Date")

    tag = st.text_input("Tag", placeholder="momentum play")
    thesis = st.text_area("Investment Thesis", placeholder="Why did you enter this trade?")
    conviction = st.selectbox("Conviction Level", ["Low", "Medium", "High"])
    target_price = st.number_input("Target Price", min_value=0.0, step=0.01)
    status = st.selectbox("Status", ["Open", "Closed"])

    submitted = st.form_submit_button("Save Trade")

    if submitted:
        trades_df = add_trade(
            trades_df=trades_df,
            ticker=ticker,
            shares=shares,
            buy_price=buy_price,
            buy_date=buy_date,
            sell_price=sell_price,
            sell_date=sell_date,
            tag=tag,
            thesis=thesis,
            conviction=conviction,
            target_price=target_price,
            status=status
        )
        save_trades(TRADES_FILE, trades_df)
        st.success("Trade added successfully!")
        st.rerun()

