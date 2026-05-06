import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_latest_price(ticker):
    """
    """