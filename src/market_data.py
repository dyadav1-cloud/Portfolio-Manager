import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data(ttl=300)
def get_latest_price(ticker):
    """
    Fetch the latest available closing price for one stock ticker.
    
    The ttl="""