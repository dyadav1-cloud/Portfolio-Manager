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
