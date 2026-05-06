import matplotlib.pyplot as plt

def plot_allocation_pie(position_df):
    """
    Create a pie chart showing portfolio allocation by ticker.

    Allocation is based on current market value, not original cost basis.
    """

    allocation_df = (
        position_df
        .groupby("ticker")["current_value"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots()

    ax.pie(
        allocation_df["current_value"],
        labels=allocation_df["ticker"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Portfolio Allocation by Current Value")

    return fig