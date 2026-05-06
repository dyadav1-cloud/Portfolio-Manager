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

    )

    fig = px.pie(
        allocation_df,
        names="ticker",
        values="current_value",
        hole=0.45,
        title="Portfolio Allocation",
        hover_data={
            "current_value": ":$,.2f",
            "cost_basis": ":$,.2f",
            "unrealized_pl": ":$,.2f"
        }
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig
