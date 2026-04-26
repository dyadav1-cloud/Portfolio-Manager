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
