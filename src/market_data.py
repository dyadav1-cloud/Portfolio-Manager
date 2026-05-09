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
def _fetch_company_info(ticker):
    """
    Fetch raw company metadata from Yahoo and cache only successful calls.
    """
    return yf.Ticker(ticker).get_info()


def get_company_overview(ticker):
    """
    Fetch the company name and business overview for one stock ticker.
    """
    default_overview = {
        "company_name": ticker,
        "company_overview": "Company overview unavailable."
    }

    try:
        ticker_info = _fetch_company_info(ticker)
    except Exception:
        return default_overview

    if not isinstance(ticker_info, dict) or not ticker_info:
        return default_overview

    company_name = (
        ticker_info.get("longName")
        or ticker_info.get("shortName")
        or ticker
    )

    company_overview = (
        ticker_info.get("longBusinessSummary")
        or ticker_info.get("description")
        or default_overview["company_overview"]
    )

    return {
        "company_name": company_name,
        "company_overview": company_overview
    }


def get_prices_for_tickers(tickers):
    """
    Fetch latest prices and company overview data for a list of tickers.
    """
    price_rows = []

    for ticker in tickers:
        latest_price = get_latest_price(ticker)
        company_data = get_company_overview(ticker)

        price_rows.append(
            {
                "ticker": ticker,
                "latest_price": latest_price,
                "company_name": company_data["company_name"],
                "company_overview": company_data["company_overview"]
            }
        )

    return pd.DataFrame(price_rows)

@st.cache_data(ttl=3600)
def get_historical_prices(tickers, start_date):
    """
    Fetch historical adjusted closing prices for multiple tickers.

    Returns a DataFrame where the index is date and each column is a ticker.
    """
    try:
        stock_data = yf.download(
            tickers,
            start=start_date,
            progress=False,
            auto_adjust=False
        )
        if stock_data.empty:
            return pd.DataFrame()
        
        if "Adj Close" in stock_data.columns:
            price_history = stock_data["Adj Close"]
        else:
            price_history = stock_data["Close"]

        if isinstance(price_history, pd.Series):
            price_history = price_history.to_frame(name=tickers[0])

        price_history = price_history.dropna(how="all")

        return price_history

    except:
        return pd.DataFrame()
    
@st.cache_data(ttl=900)
def get_market_snapshot():
    """
    Fetch a simple market snapshot for major U.S. market ETFs.

    SPY = S&P 500
    QQQ = Nasdaq 100
    DIA = Dow Jones Industrial Average
    IWM = Russell 2000
    """

    market_tickers = {
        "SPY": "S&P 500",
        "QQQ": "Nasdaq 100",
        "DIA": "Dow Jones",
        "IWM": "Russell 2000"
    }

    snapshot_rows = []

    for ticker, market_name in market_tickers.items():
        try:
            market_data = yf.download(
                ticker,
                period="5d",
                interval="1d",
                progress=False,
                auto_adjust=False
            )

            if market_data.empty:
                continue

            close_prices = market_data["Close"].dropna()

            if close_prices.empty or len(close_prices) < 2:
                continue

            latest_price = close_prices.iloc[-1]
            first_price = close_prices.iloc[0]

            if hasattr(latest_price, "iloc"):
                latest_price = latest_price.iloc[0]

            if hasattr(first_price, "iloc"):
                first_price = first_price.iloc[0]

            five_day_return = ((latest_price - first_price) / first_price) * 100

            snapshot_rows.append(
                {
                    "ticker": ticker,
                    "market": market_name,
                    "latest_price": round(float(latest_price), 2),
                    "five_day_return_percent": round(float(five_day_return), 2)
                }
            )

        except Exception:
            continue

    return pd.DataFrame(snapshot_rows)

