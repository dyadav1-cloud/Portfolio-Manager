import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import os
from data_manager import load_trades, save_trades, add_trade, delete_trade

# This block helps me move my file without having to change names each time.
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

TRADES_FILE = get_data_path("trades.csv")

st.title("Portfolio Manager")
st.write("Trade journal and performance dashboard.")


trades_df = load_trades(TRADES_FILE)

st.subheader("Saved Trades")
st.dataframe(trades_df)

if not trades_df.empty:
    st.subheader("Delete a Trade")

    trade_ids = trades_df["trade_id"].tolist()
    selected_trade_id = st.selectbox("Select Trade ID to Delete", trade_ids)

    if st.button("Delete Selected Trade"):
        trades_df = delete_trade(trades_df, selected_trade_id)
        save_trades(trades_df, TRADES_FILE)
        st.warning("Trade deleted.")
        st.rerun()



