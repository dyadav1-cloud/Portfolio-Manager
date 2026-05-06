import matplotlib.pyplot as plt

def plot_allocation_pie(position_df):
    """
    Create a pie chart showing portfolio allocation by ticker.

    Allocation is based on current market value, not original cost basis.
    """
    