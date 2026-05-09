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
```

Run the production version of the app:

streamlit run dist/main.py
File Structure
Portfolio-Manager/
├── README.md
├── requirements.txt
├── demo.mp4
├── src/
│   ├── main.py
│   ├── data_manager.py
│   ├── market_data.py
│   ├── analytics.py
│   ├── charts.py
│   ├── style.py
│   └── data/
│       └── trades.csv
└── dist/
    ├── main.py
    ├── data_manager.py
    ├── market_data.py
    ├── analytics.py
    ├── charts.py
    ├── style.py
    └── data/
        └── trades.csv
Code Organization
main.py

The main Streamlit app file. It controls the sidebar navigation, page layout, forms, charts, and displayed tables.

data_manager.py

Handles CSV-based data storage. It loads trades, saves trades, adds new trades, edits existing trades, and deletes trades.

market_data.py

Handles market data from yfinance, including latest prices, company information, historical prices, and the market snapshot.

analytics.py

Calculates portfolio metrics such as cost basis, current value, unrealized profit/loss, tag summaries, portfolio history, SPY comparison, Sharpe ratio, and max drawdown.

charts.py

Creates interactive Plotly charts for allocation, profit/loss, tag performance, portfolio history, and SPY comparison.

style.py

Adds light visual polish while keeping the app compatible with Streamlit’s light and dark themes.

Data Storage

Trade data is saved in:

dist/data/trades.csv

The app stores each trade with fields such as ticker, shares, buy price, buy date, sell price, sell date, strategy tag, investment thesis, conviction level, target price, and status.

Because the data is saved to CSV, the app can be restarted without losing saved trades.

Known Limitations
The app depends on yfinance, so market data availability may vary.
Price data is cached to reduce API calls, so values may not update instantly.
Portfolio history is estimated from saved trade data and historical prices. It is not a full brokerage-level transaction history.
The app currently focuses on stocks and ETFs, not options, crypto, or mutual funds.
Closed trade analytics are basic and could be expanded in a future version.
AI Use Statement

AI tools were used as coding assistants during development. They helped with debugging, code organization, refactoring, documentation, and feature planning. The app logic, structure, and final implementation were reviewed and tested by the developer to ensure the code was understood and could be explained.

Development Process

The project was developed progressively using GitHub and GitDoc. The app began as a simple CSV-based trade logger, then expanded into a live portfolio dashboard with market data, analytics, charts, benchmark comparison, and a guided trade journal interface.