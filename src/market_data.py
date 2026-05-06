import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_latest_price(ticker):
    """
    Fetch the latest available closing price for one stock ticker.
    
    The ttl=300 means Streamlit caches the result for 5 minutes,
    so the app does not keep hitting yfinance again and again.
    """
    try:
        stock