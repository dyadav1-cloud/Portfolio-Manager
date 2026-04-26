import streamlit as st
import os
from data_manager import load_trades, save_trades, add_trade, delete_trade

# This block helps me move my file without having to change names each time.
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(APP_PATH, "data", filename)

TRADES_FILE = get_data_path("trades.csv")

st.title("Portfolio Manager")
st.write("Trade journal and performance dashboard.")


trades_df = load_trades(TRADES_FILE)

if trades_df.empty:
    total_trades = 0
    unique_tickers = 0
    total_cost_basis = 0

else:
    trades_df["shares"] = pd.to_numeric(trades_df["shares"], errors="coerce").fillna(0)
    trades_df["buy_price"] = pd.to_numeric(trades_df["buy_price"], errors="coerce").fillna(0)

    total_trades = len(trades_df)
    uni


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
    st.subheader("Delete a Trade")

    trade_ids = trades_df["trade_id"].tolist()
    selected_trade_id = st.selectbox("Select Trade ID to Delete", trade_ids)

    if st.button("Delete Selected Trade"):
        trades_df = delete_trade(trades_df, selected_trade_id)
        save_trades(trades_df, TRADES_FILE)
        st.warning("Trade deleted.")
        st.rerun()



