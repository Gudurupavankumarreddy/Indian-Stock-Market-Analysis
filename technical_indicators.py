import mysql.connector
import pandas as pd
import pandas_ta as ta

#  Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan@123",
    database="stock_market"
)
cursor = conn.cursor()

#  Get all companies
cursor.execute("SELECT company_id, ticker FROM company_master")
companies = cursor.fetchall()

for company_id, ticker in companies:
    print(f"Processing indicators for: {ticker}")

    #  Load data for this company
    query = f"""
        SELECT date, close_price
        FROM stock_price_daily
        WHERE company_id = {company_id}
        ORDER BY date
    """
    df = pd.read_sql(query, conn)

    if df.empty:
        print(f" No data for {ticker}")
        continue

    #  Calculate Indicators
    df["sma_20"] = ta.sma(df["close_price"], length=20)
    df["sma_50"] = ta.sma(df["close_price"], length=50)
    df["ema_20"] = ta.ema(df["close_price"], length=20)
    df["ema_50"] = ta.ema(df["close_price"], length=50)
    df["rsi"] = ta.rsi(df["close_price"], length=14)
    macd = ta.macd(df["close_price"])
    df["macd"] = macd["MACD_12_26_9"]

    #  Insert into technical_indicators table
    df = df.dropna()  # remove rows where indicators are not available

    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO technical_indicators
            (company_id, date, sma_20, sma_50, ema_20, ema_50, rsi, macd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_id,
            row["date"],
            row["sma_20"],
            row["sma_50"],
            row["ema_20"],
            row["ema_50"],
            row["rsi"],
            row["macd"]
        ))

    conn.commit()
    print(f" Indicators inserted for: {ticker}")

cursor.close()
conn.close()
print(" All indicators generated successfully!")
