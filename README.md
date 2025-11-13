# Indian-Stock-Market-Analysis
Built an end-to-end forecasting system combining SQL, Python, and Power BI to predict stock price trends and identify high-growth companies in the Indian market.

👋 Hi, I’m Pavan Kumar Reddy

I’m a data analytics enthusiast passionate about turning raw data into powerful insights.
This project represents a complete data-to-decision pipeline — from data extraction to predictive visualization — built to showcase my ability to connect Python forecasting, SQL, and Power BI into one seamless workflow.

🧭 Project Overview

The goal of this project was to analyze and forecast the performance of major Indian companies across multiple sectors using historical stock data.
I combined MySQL, Python (Prophet + ARIMA), and Power BI to uncover patterns, volatility, and 365-day future predictions.

🎥 Project Demo

🎬 Watch the Dashboard Walkthrough (1:27 min)
DEMO VIDEO


| Category              | Tools / Technologies                                  |
| --------------------- | ----------------------------------------------------- |
| 💾 Database           | MySQL                                                 |
| 🐍 Programming        | Python (Pandas, NumPy, Prophet, pmdarima, Matplotlib) |
| 📊 Visualization      | Power BI                                              |
| 🔢 Analytics Language | DAX                                                   |
| 🔮 Forecasting Models | Prophet & ARIMA                                       |
| 🧰 Version Control    | GitHub                                                |

🗂️ Database Schema (MySQL)
CREATE TABLE company_master (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    ticker VARCHAR(20),
    sector VARCHAR(50)
);

CREATE TABLE stock_price_daily (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    date DATE,
    open_price DECIMAL(10,2),
    high_price DECIMAL(10,2),
    low_price DECIMAL(10,2),
    close_price DECIMAL(10,2),
    adj_close_price DECIMAL(10,2),
    volume BIGINT,
    FOREIGN KEY (company_id) REFERENCES company_master(company_id)
);

CREATE TABLE technical_indicators (
    indicator_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    date DATE,
    sma_20 DECIMAL(10,2),
    sma_50 DECIMAL(10,2),
    ema_20 DECIMAL(10,2),
    ema_50 DECIMAL(10,2),
    rsi DECIMAL(10,2),
    macd DECIMAL(10,2),
    FOREIGN KEY (company_id) REFERENCES company_master(company_id)
);


🐍 Python Components

| File                         | Purpose                                      |
| ---------------------------- | -------------------------------------------- |
| `data_download.py`           | Fetches and cleans stock price data          |
| `load_to_mysql.py`           | Loads datasets into MySQL tables             |
| `eda.py`                     | Exploratory data analysis and trend checking |
| `forecast_prophet.py`        | Prophet-based forecasting for each company   |
| `forecast_arima.py`          | ARIMA model forecasting for trend validation |
| `export_prophet_forecast.py` | Exports Prophet results to CSV               |
| `export_arima_forecast.py`   | Exports ARIMA results to CSV                 |
| `merge_stock_data.py`        | Combines all final data for Power BI input   |

🔮 Forecasting Models
⚡ Prophet (365-Day Forecast)

Models trend + seasonality for each stock

Generates future predictions (yhat, yhat_upper, yhat_lower)

Exports results to prophet_forecast_all_companies.csv

⚙️ ARIMA

Statistical validation model using auto-ARIMA

Compares results with Prophet for accuracy & consistency

Stored in arima_forecast_all_companies.csv


💾 Datasets Used
| File                                 | Description                            |
| ------------------------------------ | -------------------------------------- |
| `company_master.csv`                 | Company-level metadata                 |
| `stock_price_daily.csv`              | Daily open, close, high, low, volume   |
| `technical_indicators.csv`           | RSI, MACD, SMA, EMA                    |
| `merged_stock_data.csv`              | Consolidated dataset for visualization |
| `prophet_forecast_all_companies.csv` | Prophet 365-day forecasts              |
| `arima_forecast_all_companies.csv`   | ARIMA model validation                 |


🧮 DAX Measures Used in Power BI
| Measure                       | Description                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Total Companies**           | `COUNTROWS(company_master)`                                                                                   |
| **Total Trading Volume**      | `SUM(stock_price_daily[volume])`                                                                              |
| **Highest Close Price**       | `MAX(stock_price_daily[close_price])`                                                                         |
| **Lowest Close Price**        | `MIN(stock_price_daily[close_price])`                                                                         |
| **Highest Close per company** | `CALCULATE(MAX(stock_price_daily[close_price]), ALLEXCEPT(stock_price_daily, stock_price_daily[company_id]))` |
| **Lowest Close per company**  | `CALCULATE(MIN(stock_price_daily[close_price]), ALLEXCEPT(stock_price_daily, stock_price_daily[company_id]))` |
| **Avg Daily Volume**          | `AVERAGE(stock_price_daily[volume])`                                                                          |
| **Company Avg Close**         | `AVERAGE(stock_price_daily[close_price])`                                                                     |
| **Sector Avg Close**          | `AVERAGEX(VALUES(company_master[sector]), [Company Avg Close])`                                               |
| **Price Growth %**            | `(Last Close - First Close) / First Close * 100`                                                              |
| **Price Volatility**          | `STDEV.P(stock_price_daily[close_price])`                                                                     |
| **Price Volatility %**        | `(STDEV.P(Close) / AVERAGE(Close)) * 100`                                                                     |
| **MA Crossover Signal**       | `IF(SMA_20 > SMA_50, "Buy Signal (Bullish Crossover)", "Sell Signal (Bearish Crossover)")`                    |
| **MACD Signal**               | `IF(MACD > 0, "Bullish", "Bearish")`                                                                          |
| **RSI Status**                | `IF(RSI > 70, "Overbought", IF(RSI < 30, "Oversold", "Neutral"))`                                             |
| **Expected Growth %**         | `(Forecast - Current) / Current * 100`                                                                        |
| **MAPE (%)**                  | `Mean Absolute Percentage Error – Model Accuracy`                                                             |
| **Start Date / End Date**     | `MIN(stock_price_daily[date]) / MAX(stock_price_daily[date])`                                                 |


🧩 Power BI Data Model

📸 Data Model Overview[SCREENSHOTS "C:\Users\pavan\Desktop\stock_project\SCREENSHOTS\Screenshot 2025-11-13 124515.png"]

📊 Power BI Dashboards
🧩 Dashboard 1 – Market Trend Overview

Goal: Analyze overall market performance and sector averages.

Visuals:

KPIs: Total Companies, Trading Volume, Highest/Lowest Close

Line Chart: Close Price Trend (2019–2024)

Area Chart: Volume Trend

Bar Chart: Sector-wise Average Closing Price

📸 Dashboard Preview[SCREENSHOTS "C:\Users\pavan\Desktop\stock_project\SCREENSHOTS\Screenshot 2025-11-13 112648.png"]

🧠 Insight: Automobile sector led with the highest average close prices and consistent upward movement.


.

📈 Dashboard 2 – Company Performance & Comparative Analysis

Goal: Deep-dive into individual company metrics & performance comparison.

Visuals:

Avg Daily Volume (Clustered Bar Chart)

Top 5 Companies by Growth %

Multi-line Close Price Trend

Price Volatility Chart

📸 Dashboard Preview[SCREENSHOTS "C:\Users\pavan\Desktop\stock_project\SCREENSHOTS\Screenshot 2025-11-13 112717.png"]

🧠 Insight: Tata Motors & ICICI Bank showed strong growth; Infosys displayed stable, consistent performance.



🤖 Dashboard 3 – Technical & Predictive Analysis

Goal: Combine forecasting & technical indicators for actionable insights.

Visuals:

Prophet Forecasted Close Price (365 Days Ahead)

Buy/Sell Recommendation Summary (SMA, EMA, RSI, MACD)

Price Volatility by Sector

Expected Growth % KPI

📸 Dashboard Preview[SCREENSHOT "C:\Users\pavan\Desktop\stock_project\SCREENSHOTS\Screenshot 2025-11-13 113059.png"]

🧠 Insight: Maruti Suzuki exhibits ~138% expected growth, supported by multiple bullish crossover indicators.

📈 Key Insights Summary
| Category                    | Key Finding                           |
| --------------------------- | ------------------------------------- |
| 🏆 Top Growing Company      | Maruti Suzuki (+138% expected growth) |
| ⚙️ Most Volatile Stock      | Tata Motors                           |
| 💼 Best Performing Sector   | Automobile                            |
| 📉 Forecast Accuracy (MAPE) | ~8–12%                                |
| 📊 Overall Market Outlook   | Bullish (Positive MACD Crossovers)    |


💭 What I Learned

This project strengthened my understanding of:

Data modeling and relational database design in MySQL

Forecasting with Prophet & ARIMA

Data visualization and storytelling with Power BI

DAX calculations for financial performance analytics

It taught me how to bridge raw data with predictive insights, mirroring a real-world financial analytics workflow.


📂 Folder Structure

STOCK_PROJECT/
│
├── dataset/
│   ├── BAJAJ_FINANCE.csv
│   ├── HDFC_BANK.csv
│   └── ...
│
├── prophet_forecasts/
│   ├── Bajaj_Finance_forecast.png
│   ├── Maruti_Suzuki_forecast.png
│   └── ...
│
├── arima_forecast_all_companies.csv
├── prophet_forecast_all_companies.csv
├── merged_stock_data.csv
├── forecast_prophet.py
├── forecast_arima.py
├── merge_stock_data.py
├── load_to_mysql.py
├── Queries.sql
├── Schema.sql
└── Indian_Stock_Market_Analysis.pbix


👨‍💻 Author

Pavan Kumar Reddy
💼 Aspiring Data Analyst | Python | SQL | Power BI | ML | Time Series
📧 [gudurupavanpavankumarreddy@gmail.com]
]
🔗 [https://www.linkedin.com/in/pavankumar0415/] | [https://github.com/Gudurupavankumarreddy]

🏷️ Tags
#PowerBI #SQL #Python #Prophet #ARIMA #DataAnalytics #MachineLearning #Forecasting #StockMarket #FinancialAnalysis

