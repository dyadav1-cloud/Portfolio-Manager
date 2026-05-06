import streamlit as st
import os
import pandas as pd
from data_manager import load_trades, save_trades, add_trade, delete_trade, edit_trade
from market_data import get_prices_for_tickers
from analytics import calculate_portfolio_summary, calculate_position_metrics
from charts import plot_allocation_donut, plot_profit_loss_bar

# This block helps me move my file without having to change names each time.
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

st.set_page_config(page_title="Portfolio Manager", page_icon="📈", layout="wide")

TRADES_FILE = get_data_path("trades.csv")

st.title("Portfolio Manager")
st.write("Trade journal and performance dashboard.")


trades_df = load_trades(TRADES_FILE)
price_df = pd.DataFrame()
position_df = pd.DataFrame()

if trades_df.empty:
    total_trades = 0
    unique_tickers = 0
    total_cost_basis = 0

else:
    trades_df["shares"] = pd.to_numeric(trades_df["shares"], errors="coerce").fillna(0)
    trades_df["buy_price"] = pd.to_numeric(trades_df["buy_price"], errors="coerce").fillna(0)

    total_trades = len(trades_df)
    unique_tickers = trades_df["ticker"].nunique()
    total_cost_basis = (trades_df["buy_price"] * trades_df["shares"]).sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Trades", total_trades)
col2.metric("Unique Tickers", unique_tickers)
col3.metric("Total Cost Basis", f"${total_cost_basis:,.2f}")

st.subheader("Portfolio Overview")

if trades_df.empty:
    st.info("Add trades to see Portfolio Overview.")
else:
    unique_tickers_list = (
        trades_df["ticker"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda tickers: tickers != ""]
        .unique()
        .tolist()
    )
    price_df = get_prices_for_tickers(unique_tickers_list)
    
    position_df = calculate_position_metrics(trades_df, price_df)
    portfolio_summary = calculate_portfolio_summary(position_df)

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    summary_col1.metric(
        "Current Portfolio Value",
        f"${portfolio_summary['total_current_value']:,.2f}"
    )

    summary_col2.metric(
        "Unrealized P/L",
        f"${portfolio_summary['total_unrealized_pl']:,.2f}"
    )

    summary_col3.metric(
        "Unrealized Return",
        f"{portfolio_summary['total_unrealized_pl_percent']:,.2f}%"
    )
    
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

st.subheader("Portfolio Allocation")

allocation_fig = plot_allocation_donut(position_df)
st.plotly_chart(allocation_fig, use_container_width=True)


with st.expander("Raw market data"):
    st.dataframe(price_df, use_container_width=True)

st.subheader("Add a New Trade")

with st.form("add_trade_form"):
    ticker = st.text_input("Ticker Symbol", placeholder="AAPL")
    shares = st.number_input("Shares", min_value=0.0, step=1.0)
    buy_price = st.number_input("Buy Price", min_value=0.0, step=0.01)
    buy_date = st.date_input("Buy Date")

    sell_price = st.number_input("Sell Price", min_value=0.0, step=0.01)
    sell_date = st.date_input("Sell Date")

    tag = st.text_input("Tag", placeholder="momentum play")
    thesis = st.text_area("Investment Thesis", placeholder="Why did you enter this trade?")
    conviction = st.selectbox("Conviction Level", ["Low", "Medium", "High"])
    target_price = st.number_input("Target Price", min_value=0.0, step=0.01)
    status = st.selectbox("Status", ["Open", "Closed"])

    submitted = st.form_submit_button("Save Trade")

    if submitted:
        if ticker.strip() == "":
            st.error("Please enter a ticker symbol.")

        elif shares <= 0:
            st.error("Please enter a valid number of shares. Shares must be greater than 0.")

        elif buy_price <= 0:
            st.error("Please enter a valid buy price. Buy price must be greater than 0.")

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

if not trades_df.empty:
    st.subheader("Edit a Trade")

    edit_trade_ids = trades_df["trade_id"].astype(int).tolist()
    selected_edit_id = st.selectbox("Select Trade ID to Edit", edit_trade_ids)

    selected_trade = trades_df[trades_df["trade_id"] == selected_edit_id].iloc[0]

    with st.form("edit_trade_form"):
        edit_ticker = st.text_input("Edit Ticker", value=str(selected_trade["ticker"]))
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

        edit_buy_date = st.date_input("Edit Buy Date", value=pd.to_datetime(selected_trade["buy_date"]))

        edit_sell_price = st.number_input(
            "Edit Sell Price",
            min_value=0.0,
            step=0.01,
            value=float(selected_trade["sell_price"]) if selected_trade["sell_price"] != "" else 0.0
        )

        edit_sell_date = st.date_input(
            "Edit Sell Date",
            value=pd.to_datetime(selected_trade["sell_date"]) if selected_trade["sell_date"] != "" else pd.Timestamp.today()
        )

        edit_tag = st.text_input("Edit Tag", value=str(selected_trade["tag"]))
        edit_thesis = st.text_area("Edit Investment Thesis", value=str(selected_trade["thesis"]))

        edit_conviction = st.selectbox(
            "Edit Conviction Level",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(selected_trade["conviction"])
            if selected_trade["conviction"] in ["Low", "Medium", "High"] else 1
        )

        edit_target_price = st.number_input(
            "Edit Target Price",
            min_value=0.0,
            step=0.01,
            value=float(selected_trade["target_price"]) if selected_trade["target_price"] != "" else 0.0
        )

        edit_status = st.selectbox(
            "Edit Status",
            ["Open", "Closed"],
            index=["Open", "Closed"].index(selected_trade["status"])
            if selected_trade["status"] in ["Open", "Closed"] else 0
        )

        edit_submitted = st.form_submit_button("Save Changes")

        if edit_submitted:
            if edit_ticker.strip() == "":
                st.error("Please enter a ticker symbol.")

            elif edit_shares <= 0:
                st.error("Shares must be greater than zero.")

            elif edit_buy_price <= 0:
                st.error("Buy price must be greater than zero.")

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
    st.subheader("Delete a Trade")

    trade_ids = trades_df["trade_id"].tolist()
    selected_trade_id = st.selectbox("Select Trade ID to Delete", trade_ids)

    if st.button("Delete Selected Trade"):
        trades_df = delete_trade(trades_df, selected_trade_id)
        save_trades(trades_df, TRADES_FILE)
        st.warning("Trade deleted.")
        st.rerun()

