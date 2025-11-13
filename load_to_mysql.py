import pandas as pd
import os
import mysql.connector

#  Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan@123",
    database="stock_market"
)
cursor = conn.cursor()

#  Company details (Asian Paints removed)
company_info = {
    "RELIANCE": ("Reliance Industries", "RELIANCE.NS", "Energy"),
    "TCS": ("Tata Consultancy Services", "TCS.NS", "IT"),
    "INFOSYS": ("Infosys", "INFY.NS", "IT"),
    "HDFC_BANK": ("HDFC Bank", "HDFCBANK.NS", "Banking"),
    "ICICI_BANK": ("ICICI Bank", "ICICIBANK.NS", "Banking"),
    "KOTAK_BANK": ("Kotak Mahindra Bank", "KOTAKBANK.NS", "Banking"),
    "MARUTI": ("Maruti Suzuki", "MARUTI.NS", "Automobile"),
    "TATA_MOTORS": ("Tata Motors", "TATAMOTORS.NS", "Automobile"),
    "BAJAJ_FINANCE": ("Bajaj Finance", "BAJFINANCE.NS", "NBFC")
}

#  Clean company_master before inserting
cursor.execute("DELETE FROM company_master")
cursor.execute("ALTER TABLE company_master AUTO_INCREMENT = 1")
conn.commit()

#  Insert companies
company_ids = {}

for key, (name, ticker, sector) in company_info.items():
    cursor.execute("""
        INSERT INTO company_master (company_name, ticker, sector)
        VALUES (%s, %s, %s)
    """, (name, ticker, sector))
    conn.commit()
    company_ids[key] = cursor.lastrowid

print(" Company master table updated")

#  Insert daily stock data
for file in os.listdir("dataset"):
    if file.endswith(".csv"):
        key = file.replace(".csv", "")

        if key not in company_ids:
            print(f"⚠️ Skipping unknown file: {file}")
            continue

        company_id = company_ids[key]
        df = pd.read_csv(f"dataset/{file}")

        #  Fix missing values
        df = df.fillna(0)

        #  Remove invalid date rows
        df = df[df["Date"].notna()]
        df = df[df["Date"] != 0]
        df = df[df["Date"] != "0"]

        #  Convert to proper date format
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])  # remove invalid parse
        df["Date"] = df["Date"].dt.date

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stock_price_daily
                (company_id, date, open_price, high_price, low_price, close_price, adj_close_price, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                company_id,
                row["Date"],
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Adj Close"],
                row["Volume"]
            ))

        conn.commit()
        print(f" Inserted data for {key}")

cursor.close()
conn.close()
print(" All 9 companies loaded successfully!")

