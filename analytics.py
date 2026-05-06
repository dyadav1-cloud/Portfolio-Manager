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

