import pandas as pd
import plotly.express as px
import textwrap


def _format_overview(overview, max_chars=320, wrap_width=60):
    """
    Keep hover text readable by trimming long company descriptions.
    """
    if not isinstance(overview, str) or not overview.strip():
        return "Company overview unavailable."

    normalized = " ".join(overview.split())

    if len(normalized) > max_chars:
        normalized = normalized[:max_chars].rsplit(" ", 1)[0] + "..."

    return "<br>".join(textwrap.wrap(normalized, width=wrap_width))


def plot_allocation_donut(position_df):
    """
    Create an interactive donut chart showing portfolio allocation by ticker.

    Allocation is based on current market value.
    """
    if position_df.empty:
        fig = px.pie(
            names=["No positions"],
            values=[1],
            hole=0.45,
            title="Portfolio Allocation"
        )
        fig.update_traces(textinfo="label", hovertemplate="<extra></extra>")
        return fig

    chart_df = position_df.copy()

    if "company_name" not in chart_df.columns:
        chart_df["company_name"] = chart_df["ticker"]

    if "company_overview" not in chart_df.columns:
        chart_df["company_overview"] = "Company overview unavailable."

    allocation_df = (
        chart_df
        .groupby("ticker", as_index=False)
        .agg(
            current_value=("current_value", "sum"),
            cost_basis=("cost_basis", "sum"),
            unrealized_pl=("unrealized_pl", "sum"),
            company_name=("company_name", "first"),
            company_overview=("company_overview", "first")
        )
    )

    # Make sure these columns are truly numeric.
    numeric_columns = ["current_value", "cost_basis", "unrealized_pl"]

    for column in numeric_columns:
        allocation_df[column] = pd.to_numeric(
            allocation_df[column],
            errors="coerce"
        ).fillna(0)

    total_value = allocation_df["current_value"].sum()

    if total_value == 0:
        allocation_df["allocation_percent"] = 0
    else:
        allocation_df["allocation_percent"] = (
            allocation_df["current_value"] / total_value * 100
        )

    allocation_df["company_overview"] = allocation_df["company_overview"].apply(
        _format_overview
    )

    allocation_df["hover_text"] = allocation_df.apply(
        lambda row: (
            f"<b>{row['ticker']}</b><br>"
            f"{row['company_name']}<br><br>"
            f"<b>Company Overview</b><br>"
            f"{row['company_overview']}<br><br>"
            f"Current Value: ${row['current_value']:,.2f}<br>"
            f"Cost Basis: ${row['cost_basis']:,.2f}<br>"
            f"Unrealized P/L: ${row['unrealized_pl']:,.2f}<br>"
            f"Allocation: {row['allocation_percent']:.2f}%"
        ),
        axis=1
    )

    fig = px.pie(
        allocation_df,
        names="ticker",
        values="current_value",
        hole=0.45,
        title="Portfolio Allocation"
    )

    # Manually attach the hover data to the chart.
    fig.update_traces(
        hovertext=allocation_df["hover_text"],
        textposition="inside",
        textinfo="label+percent",
        hovertemplate="%{hovertext}<extra></extra>"
    )

    fig.update_layout(
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def plot_profit_loss_bar(position_df):
    """
    Create an interactive bar chart showing unrealized profit/loss by ticker.
    """

    if position_df.empty:
        fig = px.bar(
            x=["No positions"],
            y=[0],
            title="Unrealized P/L by Ticker"
        )
        return fig

    pl_df = (
        position_df
        .groupby("ticker", as_index=False)
        .agg(
            unrealized_pl=("unrealized_pl", "sum"),
            current_value=("current_value", "sum"),
            cost_basis=("cost_basis", "sum")
        )
    )

    numeric_columns = ["unrealized_pl", "current_value", "cost_basis"]

    for column in numeric_columns:
        pl_df[column] = pd.to_numeric(
            pl_df[column],
            errors="coerce"
        ).fillna(0)

    fig = px.bar(
        pl_df,
        x="ticker",
        y="unrealized_pl",
        title="Unrealized Profit/Loss by Ticker",
        text="unrealized_pl",
        custom_data=[
            "current_value",
            "cost_basis",
            "unrealized_pl"
        ]
    )

    fig.update_traces(
        texttemplate="$%{text:,.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Current Value: $%{customdata[0]:,.2f}<br>"
            "Cost Basis: $%{customdata[1]:,.2f}<br>"
            "Unrealized P/L: $%{customdata[2]:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Ticker",
        yaxis_title="Unrealized P/L ($)",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def plot_tag_performance_bar(tag_summary_df):
    """
    Create an interactive bar chart showing unrealized profit/loss by trade tag.
    """
    if tag_summary_df.empty:
        fig = px.bar(
            x=["No tags"],
            y=[0],
            title="Performance by Trade Tag"
        )
        return fig
    
    chart_df = tag_summary_df.copy()

    numeric_columns = [
        "total_cost_basis",
        "total_current_value",
        "total_unrealized_pl",
        "return_percent",
        "trade_count"
    ]

    for column in numeric_columns:
        chart_df[column] = pd.to_numeric(
            chart_df[column],
            errors="coerce"
        ).fillna(0)

    fig = px.bar(
        chart_df,
        x="tag",
        y="total_unrealized_pl",
        title="Unrealized Profit/Loss by Trade Tag",
        text="total_unrealized_pl",
        custom_data=[
            "total_cost_basis",
            "total_current_value",
            "total_unrealized_pl",
            "return_percent",
            "trade_count"
        ]
    )

    