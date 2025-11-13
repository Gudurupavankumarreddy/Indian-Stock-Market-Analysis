import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# Load merged file
df = pd.read_csv("merged_stock_data.csv")

# Clean dataset
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df = df.dropna(subset=["Date", "Close"])

companies = df["company_name"].unique()

for company in companies:
    print(f"\n Running ARIMA Forecast for: {company}")

    data = df[df["company_name"] == company][["Date", "Close"]].dropna()

    # Convert datatypes
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
    data = data.dropna()

    data.set_index("Date", inplace=True)

    # Fit ARIMA
    model = ARIMA(data["Close"], order=(5,1,0))
    model_fit = model.fit()

    # Forecast next 365 days
    forecast_steps = 365
    forecast_result = model_fit.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps)
    forecast_df = pd.DataFrame({"Forecast": forecast_result.predicted_mean}, index=forecast_index)

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(data.index, data["Close"], label="Historical")
    plt.plot(forecast_df.index, forecast_df["Forecast"], label="Forecast", color="red")
    plt.title(f"ARIMA Forecast - {company}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.show()
