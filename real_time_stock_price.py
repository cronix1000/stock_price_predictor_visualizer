import datetime
import pandas as pd
import requests
import json
import yfinance as yf

# Alhpa Vantage API limited to 5 requests per minute / 25 requests per day
# def real_time_price(ticker):
#     api_key = load_api_key()
#     url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}'
#     try:
#         response = requests.get(url)
#         data = response.json()
#         if 'Global Quote' in data:
#             current_price = data['Global Quote']['05. price']
#             current_price = pd.to_numeric(current_price, errors='coerce')
#             return current_price
#         else:
#             return None
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {str(e)}")
#        return None

# yfinance much less restrictive 
def real_time_price(ticker, date):
    try:
        end_date = datetime.strptime(date, "%Y-%m-%d")
        next_day = (end_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        data = yf.download(ticker, start=next_day, end=(end_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        
        if data.empty:
            raise ValueError(f"No data available for {ticker} on {next_day}")
        

        return data['Close'].iloc[-1]
    except Exception as e:
        raise ValueError(f"Could not fetch real-time price for {ticker}: {str(e)}")