import pandas as pd
import os

TRADE_COLUMNS = [
    "trade_id",
    "ticker",
    "shares",
    "buy_price",
    "buy_date",
    "sell_price",
    "sell_date",
    "tag",
    "thesis",
    "conviction",
    "target_price",
    "status"
]

def load_trades(file_path):
    """
    Load trades from a CSV file and return them as a pandas DataFrame.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return pd.DataFrame(columns=TRADE_COLUMNS)


    trades_df = pd.read_csv(file_path)

    for columns in TRADE_COLUMNS:
        if columns not in trades_df.columns:
            trades_df[columns] = ""
        
    return trades_df[TRADE_COLUMNS]

def save_trades(trades_df, file_path):
    """
    Saves the trades DataFrame to a CSV file.
    """
    trades_df.to_csv(file_path, index=False)

def get_next_trade_id(trades_df):
    """
    Create the next trade ID.

    If there are no trades yet, the first trade ID will be 1.
    Otherwise, it will be one more than the largest existing trade ID.
    """
    if trades_df.empty:
        return 1
    else:
        return trades_df["trade_id"].max() + 1
    

def add_trade(
        trades_df,
        ticker,
        shares,
        buy_price,
        buy_date,
        sell_price,
        sell_date,
        tag,
        thesis,
        conviction,
        target_price,
        status
):
    """
    Add a new trade to the trades DataFrame.
    """
    new_trade = {
        "trade_id": get_next_trade_id(trades_df),
        "ticker": ticker.upper().strip(),
        "shares": shares,
        "buy_price": buy_price,
        "buy_date": str(buy_date),
        "sell_price": sell_price,
        "sell_date": str(sell_date),
        "tag": tag.strip(),
        "thesis": thesis.strip(),
        "conviction": conviction,
        "target_price": target_price,
        "status": status
    }

    new_trade_df = pd.DataFrame([new_trade])

    updated_trades_df = pd.concat([trades_df, new_trade_df], ignore_index=True)

    return updated_trades_df

def delete_trade(trades_df, trade_id):
    """
    Delete a trade from the trades DataFrame by its trade ID.
    """
    updated_trades_df = trades_df[trades_df["trade_id"] != trade_id]

    return updated_trades_df.reset_index(drop=True)

def edit_trades(
        trades_df,
        trade_id,
        ticker,
        shares,
        buy_price,
        buy_date,
        sell_price,
        sell_date,
        tag,
        thesis,
        conviction,
        target_price,
        status
):
    """
    Edit an existing trade using its trade ID.
    """
    trade_index = trades_df[trades_df["trade_id"] == trade_id].index

    if len(trade_index) == 0:
        return trades_df
    
    row_index = trade_index[0]

    trades_df.loc[row_index, "ticker"] = ticker.upper().strip()
    trades_df.loc[row_index, "shares"] = shares
    trades_df.loc[row_index, "buy_price"] = buy_price
    trades_df.loc[row_index, "buy_date"] = str(buy_date)
    trades_df.loc[row_index, "sell_price"] = sell_price
    trades_df.loc[row_index, "sell_date"] = str(sell_date) if sell_date else ""
    trades_df.loc[row_index, "tag"] = tag.strip()
    trades_df.loc[row_index, "thesis"] = thesis.strip()
    trades_df.loc[row_index, "conviction"] = conviction
    trades_df.loc[row_index, "target_price"] = target_price
    trades_df.loc[row_index, "status"] = status

    return trades_df


