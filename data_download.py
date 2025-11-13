import yfinance as yf
import pandas as pd
import os

#  Create dataset folder
os.makedirs("dataset", exist_ok=True)

#  NSE tickers (correct spellings)
companies = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "HDFC_BANK": "HDFCBANK.NS",
    "ICICI_BANK": "ICICIBANK.NS",
    "KOTAK_BANK": "KOTAKBANK.NS",
    "MARUTI": "MARUTI.NS",
    "TATA_MOTORS": "TATAMOTORS.NS",
    "BAJAJ_FINANCE": "BAJFINANCE.NS"
}

print("Download started…")

for name, ticker in companies.items():
    try:
        print(f"Downloading {name} ({ticker})…")

        df = yf.download(
            ticker,
            start="2019-01-01",
            end="2024-12-31",
            progress=False,
            auto_adjust=False
        )

        #  Handle empty data
        if df.empty:
            print(f" No data for {name}, skipping…")
            continue

        # Ensure Date column exists
        df.reset_index(inplace=True)

        #  Add Ticker column
        df["Ticker"] = ticker

        #  Save file
        file_path = f"dataset/{name}.csv"
        df.to_csv(file_path, index=False)

        print(f" Saved: {file_path}")

    except Exception as e:
        print(f" Error downloading {name}: {e}")

print(" Dataset download complete!")
