# Portfolio Manager

A Streamlit-based portfolio tracker and trade journal that helps users record stock trades, track portfolio performance, analyze investment decisions, and compare active trades against the S&P 500 using SPY.

## Project Description

Portfolio Manager is a data-driven Python web app built with Streamlit. The app allows users to log stock trades, save them to a CSV file, fetch live market data, calculate portfolio performance, and review decision-making patterns through strategy tags and benchmark comparisons.

The app is designed as more than a basic stock tracker. It also works as a guided trade journal by asking users to record their reason for entering a trade, the main risk, their exit plan, conviction level, target price, and trade strategy type.

## Key Features

- Add, edit, and delete trades
- Save/load trade data using a CSV file
- Guided trade journal prompts
- Suggested strategy tags such as long-term hold, momentum play, dividend income, swing trade, and speculative bet
- Live price fetching using `yfinance`
- Portfolio summary metrics:
  - Total cost basis
  - Current portfolio value
  - Unrealized profit/loss
  - Unrealized return
  - Sharpe ratio
  - Max drawdown
- Interactive Plotly charts:
  - Portfolio allocation donut chart
  - Profit/loss by ticker
  - Performance by trade tag
  - Portfolio performance over time
  - Actual trade P/L vs. SPY benchmark comparison
- Market snapshot for major ETFs:
  - SPY
  - QQQ
  - DIA
  - IWM
- Sidebar navigation:
  - Dashboard
  - Trade Journal
  - Benchmarks
  - Data Tables

## What Makes This Project Unique

This project is not just a generic portfolio tracker. It combines portfolio analytics with a guided decision journal. Users do not only see whether they made or lost money; they can also analyze whether certain types of trades, strategy tags, or conviction levels are actually working.

The SPY benchmark comparison also helps users evaluate whether their individual stock picks performed better or worse than simply investing the same amount into the S&P 500 ETF.

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- yfinance
- Plotly
- Matplotlib

## How to Run the App

Install the required packages:

```bash
pip install -r requirements.txt

