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
            progress=False,
            auto_adjust=False
        )
        if stock_data.empty:
            return None

        close_prices = stock_data["Close"].dropna()

        if close_prices.empty:
            return None

        latest_price = close_prices.iloc[-1]

        # Sometimes yfinance gives a Series instead of a single number.
        if hasattr(latest_price, "iloc"):
            latest_price = latest_price.iloc[0]

        return round(float(latest_price), 2)
    
    except Exception:
        return None

@st.cache_data(ttl=86400)
def get_company_profile(ticker):
    """
    Fetch a company's display name and business summary for one ticker.
    """
    default_profile = {
        "company_name": ticker,
        "company_summary": "Company summary unavailable."
    }

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        company_name = (
            info.get("longName")
            or info.get("shortName")
            or ticker
        )

        company_summary = (
            info.get("longBusinessSummary")
            or info.get("description")
            or default_profile["company_summary"]
        )

        return {
            "company_name": company_name,
            "company_summary": company_summary
        }

    except Exception:
        return default_profile
    
def get_prices_for_tickers(tickers):
    """
    Fetch latest prices and company metadata for a list of ticker symbols.
    """
    price_rows = []

    for ticker in tickers:
        latest_price = get_latest_price(ticker)
        profile = get_company_profile(ticker)

        price_rows.append(
            {
                "ticker": ticker,
                "latest_price": latest_price,
                "company_name": profile["company_name"],
                "company_summary": profile["company_summary"]
            }
        )

    return pd.DataFrame(price_rows)
