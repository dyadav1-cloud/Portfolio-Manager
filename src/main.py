import streamlit as st
import os
import pandas as pd
from data_manager import load_trades, save_trades, add_trade, delete_trade, edit_trade
from market_data import get_prices_for_tickers, get_historical_prices, get_market_snapshot
from analytics import (
    calculate_portfolio_summary,
    calculate_position_metrics,
    calculate_tag_summary,
    calculate_portfolio_history,
    calculate_spy_comparison,
    calculate_risk_metrics
)
from charts import (
    plot_allocation_donut,
    plot_profit_loss_bar,
    plot_tag_performance_bar,
    plot_portfolio_history_line,
    plot_spy_comparison_bar
)
from style import apply_custom_style

# This block helps me move my file without having to change names each time.
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

st.set_page_config(
    page_title="Portfolio Manager",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_style()

TRADES_FILE = get_data_path("trades.csv")

STRATEGY_OPTIONS = [
    "Long-term hold",
    "Momentum play",
    "Dividend income",
    "Earnings play",
    "Swing trade",
    "Speculative bet",
    "Hedge",
    "Index alternative",
    "Custom"
]

st.sidebar.title("Portfolio Manager")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Trade Journal",
        "Benchmarks",
        "Data Tables"
    ]
)

st.title(page)

if page == "Dashboard":
    st.write("Portfolio overview, market snapshot, performance charts, and risk metrics.")

elif page == "Trade Journal":
    st.write("Add, edit, delete, and review saved trades.")

elif page == "Benchmarks":
    st.write("Compare your trades against SPY and review trade strategy performance.")

elif page == "Data Tables":
    st.write("View raw market data and calculated analysis tables.")

# Data loading
trades_df = load_trades(TRADES_FILE)
price_df = pd.DataFrame()
position_df = pd.DataFrame()
tag_summary_df = pd.DataFrame()
portfolio_history_df = pd.DataFrame()
spy_comparison_df = pd.DataFrame()
market_snapshot_df = pd.DataFrame()
risk_metrics = {
    "sharpe_ratio": 0,
    "max_drawdown_percent": 0
}
portfolio_summary = {
    "total_cost_basis": 0,
    "total_current_value": 0,
    "total_unrealized_pl": 0,
    "total_unrealized_pl_percent": 0
}

# Shared calculations
market_snapshot_df = get_market_snapshot()

total_trades = 0
unique_tickers = 0
total_cost_basis = 0

if not trades_df.empty:
    trades_df["shares"] = pd.to_numeric(
        trades_df["shares"],
        errors="coerce"
    ).fillna(0)
    trades_df["buy_price"] = pd.to_numeric(
        trades_df["buy_price"],
        errors="coerce"
    ).fillna(0)

    total_trades = len(trades_df)
    total_cost_basis = (trades_df["buy_price"] * trades_df["shares"]).sum()

    unique_tickers_list = (
        trades_df["ticker"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda tickers: tickers != ""]
        .unique()
        .tolist()
    )
    unique_tickers = len(unique_tickers_list)

    if unique_tickers_list:
        price_df = get_prices_for_tickers(unique_tickers_list)
        position_df = calculate_position_metrics(trades_df, price_df)
        portfolio_summary = calculate_portfolio_summary(position_df)
        tag_summary_df = calculate_tag_summary(position_df)

        earliest_buy_date = pd.to_datetime(
            trades_df["buy_date"],
            errors="coerce"
        ).min()

        if not pd.isna(earliest_buy_date):
            history_tickers_list = unique_tickers_list.copy()

            if "SPY" not in history_tickers_list:
                history_tickers_list.append("SPY")

            price_history_df = get_historical_prices(
                history_tickers_list,
                earliest_buy_date.strftime("%Y-%m-%d")
            )

            portfolio_history_df = calculate_portfolio_history(
                trades_df,
                price_history_df
            )
            spy_comparison_df = calculate_spy_comparison(
                trades_df,
                price_history_df
            )
            risk_metrics = calculate_risk_metrics(portfolio_history_df)


# Page rendering
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Trades", total_trades)
    col2.metric("Unique Tickers", unique_tickers)
    col3.metric("Total Cost Basis", f"${total_cost_basis:,.2f}")

    st.subheader("Market Snapshot")

    if market_snapshot_df.empty:
        st.info("Market snapshot is currently unavailable.")
    else:
        best_market = market_snapshot_df.sort_values(
            "five_day_return_percent",
            ascending=False
        ).iloc[0]

        st.write(
            f"Currently leading: **{best_market['market']}** "
            f"({best_market['ticker']}) with a "
            f"**{best_market['five_day_return_percent']:.2f}%** 5-day return."
        )

        st.dataframe(
            market_snapshot_df,
            use_container_width=True
        )

    st.subheader("Portfolio Overview")

    if trades_df.empty or position_df.empty:
        st.info("Add trades to see Portfolio Overview.")
    else:
        overview_col1, overview_col2, overview_col3, overview_col4, overview_col5 = st.columns(5)

        overview_col1.metric(
            "Portfolio Value",
            f"${portfolio_summary['total_current_value']:,.2f}"
        )

        overview_col2.metric(
            "Unrealized P/L",
            f"${portfolio_summary['total_unrealized_pl']:,.2f}"
        )

        overview_col3.metric(
            "Return",
            f"{portfolio_summary['total_unrealized_pl_percent']:,.2f}%"
        )

        overview_col4.metric(
            "Sharpe Ratio",
            f"{risk_metrics['sharpe_ratio']:,.2f}"
        )

        overview_col5.metric(
            "Max Drawdown",
            f"{risk_metrics['max_drawdown_percent']:,.2f}%"
        )

        st.divider()

        display_columns = [
            "ticker",
            "shares",
            "buy_price",
            "latest_price",
            "cost_basis",
            "current_value",
            "unrealized_pl",
            "unrealized_pl_percent",
            "tag",
            "conviction",
            "status"
        ]

        st.dataframe(
            position_df[display_columns],
            use_container_width=True
        )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Portfolio Allocation")
        allocation_fig = plot_allocation_donut(position_df)
        st.plotly_chart(allocation_fig, use_container_width=True)

    with chart_col2:
        st.subheader("Profit/Loss by Ticker")
        pl_fig = plot_profit_loss_bar(position_df)
        st.plotly_chart(pl_fig, use_container_width=True)

    tag_col, history_col = st.columns(2)

    with tag_col:
        st.subheader("Performance by Trade Tag")

        if tag_summary_df.empty:
            st.info("Add tags to your trades to see tag-based performance.")
        else:
            tag_fig = plot_tag_performance_bar(tag_summary_df)
            st.plotly_chart(tag_fig, use_container_width=True)

            with st.expander("View tag performance data"):
                st.dataframe(
                    tag_summary_df,
                    use_container_width=True
                )

    with history_col:
        st.subheader("Portfolio Over Time")

        if portfolio_history_df.empty:
            st.info("Add valid buy dates to see portfolio performance over time.")
        else:
            history_fig = plot_portfolio_history_line(portfolio_history_df)
            st.plotly_chart(history_fig, use_container_width=True)

    with st.expander("Raw market data"):
        st.dataframe(price_df, use_container_width=True)

elif page == "Benchmarks":
    st.subheader("SPY Benchmark Comparison")

    if spy_comparison_df.empty:
        st.info("SPY comparison will appear once valid trades and price history are available.")
    else:
        spy_fig = plot_spy_comparison_bar(spy_comparison_df)
        st.plotly_chart(spy_fig, use_container_width=True)

        display_spy_columns = [
            "ticker",
            "buy_date",
            "actual_cost_basis",
            "actual_current_value",
            "actual_pl",
            "actual_return_percent",
            "spy_current_value",
            "spy_pl",
            "spy_return_percent",
            "difference_vs_spy"
        ]

        with st.expander("View SPY comparison data"):
            st.dataframe(
                spy_comparison_df[display_spy_columns],
                use_container_width=True
            )

elif page == "Trade Journal":
    add_tab, manage_tab, saved_tab = st.tabs(
        ["Add Trade", "Edit/Delete", "Saved Trades"]
    )

    with add_tab:
        st.subheader("Add a New Trade")

        with st.form("add_trade_form"):
            st.write("Use this form to record a trade and the reasoning behind it.")

            ticker = st.text_input("Ticker Symbol", placeholder="AAPL")

            col1, col2 = st.columns(2)

            with col1:
                shares = st.number_input("Shares", min_value=0.0, step=1.0)
                buy_price = st.number_input("Buy Price", min_value=0.0, step=0.01)
                buy_date = st.date_input("Buy Date")

            with col2:
                target_price = st.number_input("Target Price", min_value=0.0, step=0.01)
                conviction = st.selectbox("Conviction Level", ["Low", "Medium", "High"])
                status = st.selectbox("Status", ["Open", "Closed"])

            selected_strategy = st.selectbox(
                "Strategy Type",
                STRATEGY_OPTIONS
            )

            if selected_strategy == "Custom":
                tag = st.text_input("Custom Strategy Tag", placeholder="Enter your own tag")
            else:
                tag = selected_strategy

            entry_reason = st.text_area(
                "Reason for Entry",
                placeholder="Why are you entering this trade?"
            )

            main_risk = st.text_area(
                "Main Risk",
                placeholder="What could go wrong with this trade?"
            )

            exit_plan = st.text_area(
                "Exit Plan",
                placeholder="What would make you sell or close this trade?"
            )

            thesis = (
                f"Reason for Entry: {entry_reason}\n"
                f"Main Risk: {main_risk}\n"
                f"Exit Plan: {exit_plan}"
            )

            if status == "Closed":
                st.write("Closed Trade Details")

                sell_col1, sell_col2 = st.columns(2)

                with sell_col1:
                    sell_price = st.number_input("Sell Price", min_value=0.0, step=0.01)

                with sell_col2:
                    sell_date = st.date_input("Sell Date")
            else:
                sell_price = 0.0
                sell_date = ""

            submitted = st.form_submit_button("Save Trade")

            if submitted:
                if ticker.strip() == "":
                    st.error("Please enter a ticker symbol.")

                elif shares <= 0:
                    st.error("Please enter a valid number of shares. Shares must be greater than 0.")

                elif buy_price <= 0:
                    st.error("Please enter a valid buy price. Buy price must be greater than 0.")

                elif selected_strategy == "Custom" and tag.strip() == "":
                    st.error("Please enter a custom strategy tag.")

                elif status == "Closed" and sell_price <= 0:
                    st.error("Please enter a valid sell price. Sell price must be greater than 0 for closed trades.")

                else:
                    trades_df = add_trade(
                        trades_df=trades_df,
                        ticker=ticker,
                        shares=shares,
                        buy_price=buy_price,
                        buy_date=buy_date,
                        sell_price=sell_price,
                        sell_date=sell_date,
                        tag=tag,
                        thesis=thesis,
                        conviction=conviction,
                        target_price=target_price,
                        status=status
                    )

                    save_trades(trades_df, TRADES_FILE)
                    st.success("Trade added successfully!")
                    st.rerun()
    
    st.subheader("Saved Trades")
    st.dataframe(trades_df)

    with manage_tab:
    st.subheader("Edit an Existing Trade")
    if not trades_df.empty:
        edit_trade_ids = trades_df["trade_id"].astype(int).tolist()
        selected_edit_id = st.selectbox("Select Trade ID to Edit", edit_trade_ids)

        selected_trade = trades_df[
            trades_df["trade_id"].astype(int) == selected_edit_id
        ].iloc[0]

        with st.form("edit_trade_form"):
            st.write("Update the trade details and decision notes below.")

            edit_ticker = st.text_input(
                "Edit Ticker",
                value=str(selected_trade["ticker"])
            )

            edit_col1, edit_col2 = st.columns(2)

            with edit_col1:
                edit_shares = st.number_input(
                    "Edit Shares",
                    min_value=0.0,
                    step=1.0,
                    value=float(selected_trade["shares"])
                )

                edit_buy_price = st.number_input(
                    "Edit Buy Price",
                    min_value=0.0,
                    step=0.01,
                    value=float(selected_trade["buy_price"])
                )

                edit_buy_date = st.date_input(
                    "Edit Buy Date",
                    value=pd.to_datetime(selected_trade["buy_date"])
                )

            with edit_col2:
                edit_target_price = st.number_input(
                    "Edit Target Price",
                    min_value=0.0,
                    step=0.01,
                    value=float(selected_trade["target_price"])
                    if str(selected_trade["target_price"]).strip() != ""
                    else 0.0
                )

                edit_conviction = st.selectbox(
                    "Edit Conviction Level",
                    ["Low", "Medium", "High"],
                    index=["Low", "Medium", "High"].index(selected_trade["conviction"])
                    if selected_trade["conviction"] in ["Low", "Medium", "High"]
                    else 1
                )

                edit_status = st.selectbox(
                    "Edit Status",
                    ["Open", "Closed"],
                    index=["Open", "Closed"].index(selected_trade["status"])
                    if selected_trade["status"] in ["Open", "Closed"]
                    else 0
                )

            current_tag = str(selected_trade["tag"])

            if current_tag in STRATEGY_OPTIONS:
                default_strategy_index = STRATEGY_OPTIONS.index(current_tag)
            else:
                default_strategy_index = STRATEGY_OPTIONS.index("Custom")

            edit_selected_strategy = st.selectbox(
                "Edit Strategy Type",
                STRATEGY_OPTIONS,
                index=default_strategy_index
            )

            if edit_selected_strategy == "Custom":
                edit_tag = st.text_input(
                    "Edit Custom Strategy Tag",
                    value=current_tag if current_tag not in STRATEGY_OPTIONS else ""
                )
            else:
                edit_tag = edit_selected_strategy

            edit_thesis = st.text_area(
                "Edit Investment Thesis",
                value=str(selected_trade["thesis"])
            )

            if edit_status == "Closed":
                st.write("Closed Trade Details")

                edit_sell_col1, edit_sell_col2 = st.columns(2)

                with edit_sell_col1:
                    edit_sell_price = st.number_input(
                        "Edit Sell Price",
                        min_value=0.0,
                        step=0.01,
                        value=float(selected_trade["sell_price"])
                        if str(selected_trade["sell_price"]).strip() != ""
                        else 0.0
                    )

                with edit_sell_col2:
                    if str(selected_trade["sell_date"]).strip() != "":
                        edit_sell_date_value = pd.to_datetime(selected_trade["sell_date"])
                    else:
                        edit_sell_date_value = pd.Timestamp.today()

                    edit_sell_date = st.date_input(
                        "Edit Sell Date",
                        value=edit_sell_date_value
                    )
            else:
                edit_sell_price = 0.0
                edit_sell_date = ""

            edit_submitted = st.form_submit_button("Save Changes")

            if edit_submitted:
                if edit_ticker.strip() == "":
                    st.error("Please enter a ticker symbol.")

                elif edit_shares <= 0:
                    st.error("Shares must be greater than zero.")

                elif edit_buy_price <= 0:
                    st.error("Buy price must be greater than zero.")

                elif edit_selected_strategy == "Custom" and edit_tag.strip() == "":
                    st.error("Please enter a custom strategy tag.")

                elif edit_status == "Closed" and edit_sell_price <= 0:
                    st.error("Closed trades need a sell price.")

                else:
                    trades_df = edit_trade(
                        trades_df=trades_df,
                        trade_id=selected_edit_id,
                        ticker=edit_ticker,
                        shares=edit_shares,
                        buy_price=edit_buy_price,
                        buy_date=edit_buy_date,
                        sell_price=edit_sell_price,
                        sell_date=edit_sell_date,
                        tag=edit_tag,
                        thesis=edit_thesis,
                        conviction=edit_conviction,
                        target_price=edit_target_price,
                        status=edit_status
                    )

                    save_trades(trades_df, TRADES_FILE)
                    st.success("Trade updated successfully!")
                    st.rerun()


    if not trades_df.empty:
        with st.expander("Delete a Trade"):
            st.subheader("Delete a Trade")

            trade_ids = trades_df["trade_id"].tolist()
            selected_trade_id = st.selectbox("Select Trade ID to Delete", trade_ids)

            if st.button("Delete Selected Trade"):
                trades_df = delete_trade(trades_df, selected_trade_id)
                save_trades(trades_df, TRADES_FILE)
                st.warning("Trade deleted.")
                st.rerun()

elif page == "Data Tables":
    with st.expander("Trades Table", expanded=True):
        st.dataframe(trades_df, use_container_width=True)

    with st.expander("Latest Prices Table"):
        st.dataframe(price_df, use_container_width=True)

    with st.expander("Position Metrics Table"):
        st.dataframe(position_df, use_container_width=True)

    with st.expander("Tag Summary Table"):
        st.dataframe(tag_summary_df, use_container_width=True)

    with st.expander("Portfolio History Table"):
        st.dataframe(portfolio_history_df, use_container_width=True)

    with st.expander("SPY Comparison Table"):
        st.dataframe(spy_comparison_df, use_container_width=True)

    with st.expander("Market Snapshot Table"):
        st.dataframe(market_snapshot_df, use_container_width=True)
