import datetime
from matplotlib import pyplot as plt
import pandas as pd
import yfinance as yf

from predict_price import predict_price_movement
from stock_data_ai import train_regression_model


def run_for_large_ammount():
    # default_tickers = [
    #     'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META',
    #     'NVDA', 'TSLA', 'JPM', 'V', 'WMT'
    # ]

    default_tickers = [
        'AAPL', 'GOOGL'
    ]
    
    initial_start_date = datetime.datetime(2020, 11, 29)
    months_to_check = 12  

    compiled_data = []

    for ticker in default_tickers:
        for month in range(months_to_check):
            start_date = initial_start_date + datetime.timedelta(days=month * 30)
            end_date = start_date + datetime.timedelta(days=30)

            data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
            if data.empty:
                print(f"No data available for {ticker} between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}")
                continue

            # Checks if the previous day's open price is less than the current day's open price
            data['open_price'] = (data['Open'].shift(-1) > data['Open']).astype(int)
            data = data.dropna()

            print(data)

            model = train_regression_model(data)

            # Gets the last row of data or the last in the dataset, checks to see if the price will go up or down
            features = data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1].values.reshape(1, -1)

            prediction = predict_price_movement(model, features)

            # Gets the last row of the data and checks the actual price movement
            actual = data['open_price'].iloc[-1]

            compiled_data.append({
                'Ticker': ticker,
                'Start Date': start_date.strftime('%Y-%m-%d'),
                'End Date': end_date.strftime('%Y-%m-%d'),
                'Prediction': prediction,
                'Actual': actual
            })

            print(f"Prediction: {prediction}, Actual: {actual}")

    compiled_df = pd.DataFrame(compiled_data)

    for ticker in default_tickers:
        ticker_data = compiled_df[compiled_df['Ticker'] == ticker]
        plt.figure(figsize=(10, 5))
        plt.plot(ticker_data['Start Date'], ticker_data['Prediction'], label='Prediction', marker='o')
        plt.plot(ticker_data['Start Date'], ticker_data['Actual'], label='Actual', marker='x')
        plt.title(f'Predictions vs Actual for {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Direction')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    run_for_large_ammount()