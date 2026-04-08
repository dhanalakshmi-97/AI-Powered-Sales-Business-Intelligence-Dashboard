import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("clean_data.csv")

# Convert date
df['Order Date'] = pd.to_datetime(df['Order Date'])

print("Data Loaded Successfully")
#print(df.columns)


def generate_kpis():
    total_sales = df['Sum of Sales'].sum()
    total_profit = df['Sum of Profit'].sum()
    total_orders = df['Order ID'].nunique()
    best_region = df.groupby("Region")["Sum of Sales"].sum().idxmax()


    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Best Region": best_region
    }

def detect_anomalies():
    df['zscore'] = (
        df['Sum of Sales'] - df['Sum of Sales'].mean()
    ) / df['Sum of Sales'].std()

    anomalies = df[df['zscore'] > 3]
    return anomalies

def monthly_sales():
    monthly = df.groupby(df['Order Date'].dt.to_period("M"))['Sum of Sales'].sum()
    return monthly


def predict_sales():
    monthly = df.groupby(df['Order Date'].dt.to_period("M"))['Sum of Sales'].sum()
    monthly = monthly.reset_index()

    monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()
    monthly['MonthIndex'] = range(len(monthly))

    X = monthly[['MonthIndex']]
    y = monthly['Sum of Sales']

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[len(monthly)]]
    prediction = model.predict(next_month)

    return prediction[0]