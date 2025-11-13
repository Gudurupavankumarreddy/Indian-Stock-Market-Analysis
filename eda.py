import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

#  MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan@123",
    database="stock_market"
)

#  Load all STOCK DATA
query = """
SELECT c.company_name, s.*
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
ORDER BY s.date;
"""
df = pd.read_sql(query, conn)

print(" Data Loaded for EDA")
print(df.head())

# -----------------------------------------
#  1. LINE CHART: Close Price Trend
# -----------------------------------------

plt.figure(figsize=(12,6))
for comp in df["company_name"].unique():
    subset = df[df["company_name"] == comp]
    plt.plot(subset["date"], subset["close_price"], label=comp)

plt.title("Close Price Trend")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.grid(True)
plt.show()

# -----------------------------------------
#  2. VOLUME TREND
# -----------------------------------------

plt.figure(figsize=(12,6))
for comp in df["company_name"].unique():
    subset = df[df["company_name"] == comp]
    plt.plot(subset["date"], subset["volume"], label=comp)

plt.title("Volume Trend")
plt.xlabel("Date")
plt.ylabel("Trading Volume")
plt.legend()
plt.grid(True)
plt.show()

# -----------------------------------------
#  3. CORRELATION HEATMAP (Close prices)
# -----------------------------------------

pivot_df = df.pivot(index="date", columns="company_name", values="close_price")

plt.figure(figsize=(10,6))
sns.heatmap(pivot_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Between Companies")
plt.show()

# -----------------------------------------
#  4. CANDLESTICK CHART (Choose ONE)
# -----------------------------------------

company = "Reliance Industries"   #  change if needed
sub = df[df["company_name"] == company]

fig = go.Figure(data=[go.Candlestick(
    x=sub["date"],
    open=sub["open_price"],
    high=sub["high_price"],
    low=sub["low_price"],
    close=sub["close_price"]
)])

fig.update_layout(title=f"Candlestick Chart - {company}", xaxis_rangeslider_visible=False)
fig.show()

# -----------------------------------------
#  5. TECHNICAL INDICATOR OVERLAY (SMA & EMA)
# -----------------------------------------

ti_query = """
SELECT c.company_name, t.*
FROM technical_indicators t
JOIN company_master c ON t.company_id = c.company_id
ORDER BY t.date;
"""

ti_df = pd.read_sql(ti_query, conn)

company = "Reliance Industries"
sub = ti_df[ti_df["company_name"] == company]

plt.figure(figsize=(12,6))
plt.plot(sub["date"], sub["sma_20"], label="SMA 20")
plt.plot(sub["date"], sub["sma_50"], label="SMA 50")
plt.plot(sub["date"], sub["ema_20"], label="EMA 20")
plt.plot(sub["date"], sub["ema_50"], label="EMA 50")
plt.title(f"Technical Indicators for {company}")
plt.legend()
plt.grid(True)
plt.show()
