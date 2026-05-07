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

def plot_tag_performance_bar(tag_summary_df):
    """
    Create an interactive bar chart showing unrealized profit/loss by trade tag.
    """
    