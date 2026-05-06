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
        stock_data = yf.download(
            ticker,
            period = "5d",
            interval="1d",
            progress=False
        )
        if stock_data.empty:
            return None
        
        latest_price = stock_data["Close"].dropna().iloc[-1]
        return round(float(latest_price), 2)
    
    except Exception:
        return None
    
def get_prices_for_tickers(tickers):
    """
    Fetch latest prices for a list of ticker symbols.
    Returns a DataFrame with ticker and latest_price columns.
    """
    price_rows = []
