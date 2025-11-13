import mysql.connector
import pandas as pd
from prophet import Prophet

#  MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pavan@123",
    database="stock_market"
)

cursor = conn.cursor()
cursor.execute("SELECT company_name FROM company_master")
companies = [row[0] for row in cursor.fetchall()]

all_results = []

for company in companies:
    print("Processing Prophet forecast for:", company)

    query = f"""
    SELECT s.date, s.close_price
    FROM stock_price_daily s
    JOIN company_master c ON s.company_id = c.company_id
    WHERE c.company_name = '{company}'
    ORDER BY s.date;
    """

    df = pd.read_sql(query, conn)
    df = df.rename(columns={"date": "ds", "close_price": "y"})

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    forecast["company_name"] = company

    all_results.append(
        forecast[["company_name", "ds", "yhat", "yhat_lower", "yhat_upper"]]
    )

#  Save as CSV
final_df = pd.concat(all_results)
final_df.to_csv("prophet_forecast_all_companies.csv", index=False)
