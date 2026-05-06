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
