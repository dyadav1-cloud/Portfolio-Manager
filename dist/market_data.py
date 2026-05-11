import pandas as pd
import yfinance as yf
import streamlit as st


# ttl=300 means this result is cached for 5 minutes before yfinance is called again.
# Without caching, every chart render would trigger a new network request.
@st.cache_data(ttl=300)
def get_latest_price(ticker):
    """
    Fetch the latest available closing price for one stock ticker using yfinance.

    Downloads the last 5 days of daily data and returns the most recent close price.
    Returns None if the data is unavailable — the caller handles this with fillna(0).

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
        # If yfinance throws any error (network issue, bad ticker, etc.), return None
        # so the rest of the app can fall back to showing 0 or a placeholder.
        return None


# ttl=86400 caches company info for 24 hours since it rarely changes.
@st.cache_data(ttl=86400)
def _fetch_company_info(ticker):
    """
    Fetch raw company metadata from Yahoo Finance and cache only successful calls.

    This is a private helper so that get_company_overview can handle errors without
    caching failed responses (Streamlit only caches successful return values).
    """
    return yf.Ticker(ticker).get_info()


def get_company_overview(ticker):
    """
    Fetch the company name and business overview for one stock ticker.

    Returns a dict with 'company_name' and 'company_overview'.
    Falls back to safe default strings if the data is unavailable,
    so charts and hover text always have something to show.
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

    Calls get_latest_price and get_company_overview for each ticker and combines
    the results into a single DataFrame. Rows with missing prices will have None
    in the latest_price column — analytics.py handles that with fillna(0).
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

# ttl=3600 caches historical prices for 1 hour since intraday changes don't matter here.
@st.cache_data(ttl=3600)
def get_historical_prices(tickers, start_date):
    """
    Fetch historical adjusted closing prices for multiple tickers using yfinance.

    Returns a DataFrame where the index is the date and each column is a ticker symbol.
    Uses 'Adj Close' when available (adjusts for stock splits and dividends), otherwise
    falls back to 'Close'. Returns an empty DataFrame if the download fails.
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

        # If only one ticker was passed, yfinance returns a Series. Wrap it in a DataFrame.
        if isinstance(price_history, pd.Series):
            price_history = price_history.to_frame(name=tickers[0])

        price_history = price_history.dropna(how="all")

        return price_history

    except:
        # Return an empty DataFrame on any error so the app degrades gracefully.
        return pd.DataFrame()

# ttl=900 caches the market snapshot for 15 minutes.
@st.cache_data(ttl=900)
def get_market_snapshot():
    """
    Fetch a simple 5-day price snapshot for four major U.S. market ETFs.

    Uses yfinance to download 5 days of daily closing prices for each ETF
    and calculates the percentage return from the first day to the last.

    SPY = S&P 500
    QQQ = Nasdaq 100
    DIA = Dow Jones Industrial Average
    IWM = Russell 2000

    Tickers that fail to download are skipped with 'continue' so one bad
    ticker doesn't prevent the others from appearing.
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

            # Need at least 2 data points to calculate a return.
            if close_prices.empty or len(close_prices) < 2:
                continue

            latest_price = close_prices.iloc[-1]
            first_price = close_prices.iloc[0]

            if hasattr(latest_price, "iloc"):
                latest_price = latest_price.iloc[0]

            if hasattr(first_price, "iloc"):
                first_price = first_price.iloc[0]

            # 5-day return = (end price - start price) / start price × 100
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
