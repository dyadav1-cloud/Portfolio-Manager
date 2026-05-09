import pandas as pd

def calculate_position_metrics(trades_df, price_df):
    """
    Combine saved trades with live price data and calculate basic
    portfolio metrics for each position.
    """
    if trades_df.empty:
        return trades_df

    position_df = trades_df.merge(
        price_df,
        on="ticker",
        how="left"
    )

    position_df["shares"] = pd.to_numeric(
        position_df["shares"],
        errors="coerce"
    ).fillna(0)

    position_df["buy_price"] = pd.to_numeric(
        position_df["buy_price"],
        errors="coerce"
    ).fillna(0)

    position_df["latest_price"] = pd.to_numeric(
        position_df["latest_price"],
        errors="coerce"
    ).fillna(0)

    position_df["cost_basis"] = (
        position_df["shares"] * position_df["buy_price"]
    )

    position_df["current_value"] = (
        position_df["shares"] * position_df["latest_price"]
    )

    position_df["unrealized_pl"] = (
        position_df["current_value"] - position_df["cost_basis"]
    )

    position_df["unrealized_pl_percent"] = (
        position_df["unrealized_pl"] / position_df["cost_basis"] * 100
    )

    position_df["unrealized_pl_percent"] = (
        position_df["unrealized_pl_percent"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    return position_df

def calculate_portfolio_summary(position_df):
    """
    Calculate portfolio-level summary metrics from the position table.
    """

    if position_df.empty:
        return {
            "total_cost_basis": 0,
            "total_current_value": 0,
            "total_unrealized_pl": 0,
            "total_unrealized_pl_percent": 0
        }

    total_cost_basis = position_df["cost_basis"].sum()
    total_current_value = position_df["current_value"].sum()
    total_unrealized_pl = position_df["unrealized_pl"].sum()

    if total_cost_basis == 0:
        total_unrealized_pl_percent = 0

    else:
        total_unrealized_pl_percent = (
            total_unrealized_pl / total_cost_basis
        ) * 100

    return {
        "total_cost_basis": total_cost_basis,
        "total_current_value": total_current_value,
        "total_unrealized_pl": total_unrealized_pl,
        "total_unrealized_pl_percent": total_unrealized_pl_percent
    }

def calculate_tag_summary(position_df):
    """
    Summarize portfolio performance by trade tag.
    """
    if position_df.empty or "tag" not in position_df.columns:
        return pd.DataFrame()

    tag_df = position_df.copy()

    tag_df["tag"] = (
        tag_df["tag"]
        .fillna("Untagged")
        .astype(str)
        .str.strip()
    )

    tag_df.loc[tag_df["tag"] == "", "tag"] = "Untagged"

    tag_summary_df = (
        tag_df
        .groupby("tag", as_index=False)
        .agg(
            total_cost_basis=("cost_basis", "sum"),
            total_current_value=("current_value", "sum"),
            total_unrealized_pl=("unrealized_pl", "sum"),
            trade_count=("trade_id", "count")
        )
    )

    tag_summary_df["return_percent"] = (
        tag_summary_df["total_unrealized_pl"]
        / tag_summary_df["total_cost_basis"]
        * 100
    )

    tag_summary_df["return_percent"] = (
        tag_summary_df["return_percent"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    return tag_summary_df

def calculate_portfolio_history(trades_df, price_history_df):
    """
    Estimate portfolio value, cost basis, and unrealized P/L over time.

    For each date, this function includes only trades that were already bought
    on or before that date.
    """
    if trades_df.empty or price_history_df.empty:
        return pd.DataFrame()

    history_rows = []
    trades_copy = trades_df.copy()

    trades_copy["buy_date"] = pd.to_datetime(
        trades_copy["buy_date"],
        errors="coerce"
    )

    trades_copy["shares"] = pd.to_numeric(
        trades_copy["shares"],
        errors="coerce"
    ).fillna(0)

    trades_copy["buy_price"] = pd.to_numeric(
        trades_copy["buy_price"],
        errors="coerce"
    ).fillna(0)

    for current_date in price_history_df.index:
        active_trades = trades_copy[
            trades_copy["buy_date"] <= current_date
        ]

        total_value = 0
        total_cost_basis = 0

        for _, trade in active_trades.iterrows():
            ticker = trade["ticker"]
            shares = trade["shares"]
            buy_price = trade["buy_price"]

            if ticker in price_history_df.columns:
                current_price = price_history_df.loc[current_date, ticker]

                if pd.notna(current_price):
                    total_value += shares * current_price
                    total_cost_basis += shares * buy_price

        unrealized_pl = total_value - total_cost_basis

        if total_cost_basis == 0:
            unrealized_return_percent = 0
        else:
            unrealized_return_percent = (
                unrealized_pl / total_cost_basis
            ) * 100

        history_rows.append(
            {
                "date": current_date,
                "portfolio_value": total_value,
                "cost_basis": total_cost_basis,
                "unrealized_pl": unrealized_pl,
                "unrealized_return_percent": unrealized_return_percent
            }
        )

    return pd.DataFrame(history_rows)

def calculate_spy_comparison(trades_df, price_history_df):
    """
    Compare each trade's actual return against the return the user
    would have earned by buying SPY on the same buy date.

    This uses historical prices from price_history_df, which should include
    both the trade tickers and SPY.
    """

    if trades_df.empty or price_history_df.empty or "SPY" not in price_history_df.columns:
        return pd.DataFrame()

    comparison_rows = []

    trades_copy = trades_df.copy()

    trades_copy["buy_date"] = pd.to_datetime(
        trades_copy["buy_date"],
        errors="coerce"
    )

    trades_copy["shares"] = pd.to_numeric(
        trades_copy["shares"],
        errors="coerce"
    ).fillna(0)

    trades_copy["buy_price"] = pd.to_numeric(
        trades_copy["buy_price"],
        errors="coerce"
    ).fillna(0)

    latest_date = price_history_df.index.max()

    for _, trade in trades_copy.iterrows():
        ticker = trade["ticker"]
        buy_date = trade["buy_date"]
        shares = trade["shares"]
        buy_price = trade["buy_price"]

        if pd.isna(buy_date) or ticker not in price_history_df.columns:
            continue

        available_dates = price_history_df.index[
            price_history_df.index >= buy_date
        ]

        if len(available_dates) == 0:
            continue

        first_available_date = available_dates[0]

        ticker_buy_price = price_history_df.loc[first_available_date, ticker]
        ticker_latest_price = price_history_df.loc[latest_date, ticker]

        spy_buy_price = price_history_df.loc[first_available_date, "SPY"]
        spy_latest_price = price_history_df.loc[latest_date, "SPY"]

        if (
            pd.isna(ticker_buy_price)
            or pd.isna(ticker_latest_price)
            or pd.isna(spy_buy_price)
            or pd.isna(spy_latest_price)
        ):
            continue

        actual_current_value = shares * ticker_latest_price
        actual_cost_basis = shares * buy_price
        actual_pl = actual_current_value - actual_cost_basis

        spy_equivalent_shares = actual_cost_basis / spy_buy_price
        spy_current_value = spy_equivalent_shares * spy_latest_price
        spy_pl = spy_current_value - actual_cost_basis

        actual_return_percent = (
            actual_pl / actual_cost_basis * 100
            if actual_cost_basis != 0 else 0
        )

        spy_return_percent = (
            spy_pl / actual_cost_basis * 100
            if actual_cost_basis != 0 else 0
        )

        difference_vs_spy = actual_pl - spy_pl

        comparison_rows.append(
            {
                "trade_id": trade["trade_id"],
                "ticker": ticker,
                "buy_date": buy_date,
                "actual_cost_basis": actual_cost_basis,
                "actual_current_value": actual_current_value,
                "actual_pl": actual_pl,
                "actual_return_percent": actual_return_percent,
                "spy_current_value": spy_current_value,
                "spy_pl": spy_pl,
                "spy_return_percent": spy_return_percent,
                "difference_vs_spy": difference_vs_spy
            }
        )

    return pd.DataFrame(comparison_rows)

def calculate_risk_metrics(portfolio_history_df):
    """
    Calculate risk metrics from the portfolio history.

    Sharpe ratio measures return compared to volatility.
    Max drawdown measures the largest percentage drop from a previous peak.
    """
    if portfolio_history_df.empty or "portfolio_value" not in portfolio_history_df.columns:
        return {
            "sharpe_ratio": 0,
            "max_drawdown_percent": 0
        }
    
    history_df = portfolio_history_df.copy()

    history_df["portfolio_value"] = pd.to_numeric(
        history_df["portfolio_value"],
        errors="coerce"
    ).fillna(0)

    



    

