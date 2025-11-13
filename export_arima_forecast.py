import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

#  Load merged dataset
df = pd.read_csv("merged_stock_data.csv")

#  Clean data
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df = df.dropna(subset=["Date", "Close"])

companies = df["company_name"].unique()
all_results = []

for company in companies:
    print(f"\n Running ARIMA for: {company}")

    #  Extract company data
    data = df[df["company_name"] == company][["Date", "Close"]].dropna()

    if len(data) < 100:  
        print(f" Skipping {company} — not enough data (rows: {len(data)})")
        continue

    data = data.set_index("Date")

    try:
        #  Fit ARIMA(5,1,0)
        model = ARIMA(data["Close"], order=(5, 1, 0))
        fit = model.fit()

        #  Forecast next 365 days
        forecast_steps = 365
        forecast = fit.get_forecast(steps=forecast_steps)

        forecast_index = pd.date_range(
            data.index[-1] + pd.Timedelta(days=1),
            periods=forecast_steps
        )

        result_df = pd.DataFrame({
            "company_name": company,
            "date": forecast_index,
            "forecast": forecast.predicted_mean
        })

        all_results.append(result_df)
        print(f" Forecast generated for: {company}")

    except Exception as e:
        print(f" Error for {company}: {e}")
        continue

#  Save final CSV
if all_results:
    final_df = pd.concat(all_results)
    final_df.to_csv("arima_forecast_all_companies.csv", index=False)
    print("\n ARIMA forecast saved as: arima_forecast_all_companies.csv")
else:
    print("\n No forecasts generated!")
