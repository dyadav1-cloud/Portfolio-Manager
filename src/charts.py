import pandas as pd
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

    allocation_df["current_value"] = pd.to_numeric(
        allocation_df["current_value"],
        errors="coerce"
    ).fillna(0)

    allocation_df["cost_basis"] = pd.to_numeric(
        allocation_df["cost_basis"],
        errors="coerce"
    ).fillna(0)

    allocation_df["unrealized_pl"] = pd.to_numeric(
        allocation_df["unrealized_pl"],
        errors="coerce"
    ).fillna(0)

    total_value = allocation_df["current_value"].sum()

    if total_value == 0:
        allocation_df["allocation_percent"] = 0
    else:
        allocation_df["allocation_percent"] = (
            allocation_df["current_value"] / total_value * 100
        )

    fig = px.pie(
        allocation_df,
        names="ticker",
        values="current_value",
        hole=0.45,
        title="Portfolio Allocation",
        custom_data=[
            "current_value",
            "cost_basis",
            "unrealized_pl",
            "allocation_percent"
        ]
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Current Value: $%{customdata[0]:,.2f}<br>"
            "Cost Basis: $%{customdata[1]:,.2f}<br>"
            "Unrealized P/L: $%{customdata[2]:,.2f}<br>"
            "Allocation: %{customdata[3]:.2f}%"
            "<extra></extra>"
        )
    )



    fig.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig
