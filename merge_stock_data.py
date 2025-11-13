import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan@123",
    database="stock_market"
)

query = """
SELECT 
    c.company_id,
    c.company_name,
    c.ticker,
    c.sector,
    s.date,
    s.open_price,
    s.high_price,
    s.low_price,
    s.close_price,
    s.adj_close_price,
    s.volume
FROM stock_price_daily s
JOIN company_master c ON s.company_id = c.company_id
ORDER BY c.company_id, s.date;
"""

df = pd.read_sql(query, conn)
df.to_csv("merged_stock_data.csv", index=False)

print(" NEW merged_stock_data.csv created correctly!")
