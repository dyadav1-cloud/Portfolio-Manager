import pandas as pd
import plotly.express as px
import textwrap


def _format_company_summary(summary, max_chars=280, line_width=55):
    """
    Trim long summaries and add line breaks so hover text stays readable.
    """
    if not isinstance(summary, str) or not summary.strip():
        return "Company summary unavailable."

    normalized_summary = " ".join(summary.split())

    if len(normalized_summary) > max_chars:
        truncated = normalized_summary[: max_chars - 3].rsplit(" ", 1)[0]
        normalized_summary = f"{truncated}..."

    wrapped_lines = textwrap.wrap(normalized_summary, width=line_width)
    return "<br>".join(wrapped_lines) if wrapped_lines else normalized_summary


def plot_allocation_donut(position_df):
    """
    Create an interactive donut chart showing portfolio allocation by ticker.

    Allocation is based on current market value.
    """
    if position_df.empty:
        fig = px.pie(
            names=["No positions yet"],
            values=[1],
            hole=0.45,
            title="Portfolio Allocation"
        )
        fig.update_traces(textinfo="label", hovertemplate="<extra></extra>")
        return fig

    chart_df = position_df.copy()

    if "company_name" not in chart_df.columns:
        chart_df["company_name"] = chart_df["ticker"]

    if "company_summary" not in chart_df.columns:
        chart_df["company_summary"] = "Company summary unavailable."

    allocation_df = (
        chart_df
        .groupby("ticker", as_index=False)
        .agg(
            current_value=("current_value", "sum"),
            cost_basis=("cost_basis", "sum"),
            unrealized_pl=("unrealized_pl", "sum"),
            company_name=("company_name", "first"),
            company_summary=("company_summary", "first")
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

    allocation_df["formatted_summary"] = allocation_df["company_summary"].apply(
        _format_company_summary
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
        customdata=allocation_df[
            [
                "current_value",
                "cost_basis",
                "unrealized_pl",
                "allocation_percent",
                "company_name",
                "formatted_summary"
            ]
        ].to_numpy(),
        textposition="inside",
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{customdata[4]}<br><br>"
            "%{customdata[5]}<br><br>"
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
