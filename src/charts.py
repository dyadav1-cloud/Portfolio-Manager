import plotly.express as px

def plot_allocation_donut(position_df):
    """
    Create an interactive donut chart showing portfolio allocation by ticker.

    Allocation is based on current market value.
    """
    allocation_df = (
        position_df
        .groupby("ticker", as_index=False)
        .agg(
            current_value=("current_value", "sum"),
            cost_basis=("cost_basis", "sum"),
            unrealized_pl=("unrealized_pl", "sum")
        )


