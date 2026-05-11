import pandas as pd
import os

# The canonical list of column names for the trades CSV.
# All functions use this list to ensure the DataFrame always has consistent columns.
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

    If the file doesn't exist or is empty, returns an empty DataFrame with
    the correct columns so the rest of the app doesn't break on the first run.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return pd.DataFrame(columns=TRADE_COLUMNS)


    trades_df = pd.read_csv(file_path)

    # If the CSV was saved by an older version of the app that didn't have all
    # columns, add any missing ones with empty values so nothing errors out.
    for columns in TRADE_COLUMNS:
        if columns not in trades_df.columns:
            trades_df[columns] = ""

    return trades_df[TRADE_COLUMNS]

def save_trades(trades_df, file_path):
    """
    Save the trades DataFrame to a CSV file.

    index=False prevents pandas from writing the row numbers as a column,
    which would create an unwanted extra column when the file is loaded back.
    """
    trades_df.to_csv(file_path, index=False)

def get_next_trade_id(trades_df):
    """
    Return the next available trade ID.

    If there are no trades yet, the first trade ID will be 1.
    Otherwise, it will be one more than the largest existing trade ID.
    This avoids reusing IDs even after trades are deleted.
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
    Add a new trade row to the trades DataFrame and return the updated DataFrame.

    The original DataFrame is not modified in place — pd.concat creates a new one.
    The trade ID is assigned automatically by get_next_trade_id.
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
    Remove a trade from the DataFrame by its trade ID and return the updated DataFrame.

    reset_index(drop=True) re-numbers the DataFrame index from 0 so there are
    no gaps left after the deletion.
    """
    updated_trades_df = trades_df[trades_df["trade_id"] != trade_id]

    return updated_trades_df.reset_index(drop=True)

def edit_trade(
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
    Update an existing trade in the DataFrame using its trade ID.

    Finds the row with the matching trade_id and overwrites each field.
    If no matching trade is found, the DataFrame is returned unchanged.
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


