import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import datetime as dt
import yfinance as yf
from textblob import TextBlob
from datetime import datetime
from sklearn.metrics import accuracy_score, classification_report

def train_regression_model(data):

    # MA = Moving Average
    # MA5 = 5 day moving average
    # MA10 = 10 day moving average
    # Volatility = High - Low
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA10'] = data['Close'].rolling(window=10).mean()
    data['Price_Change'] = data['Close'] - data['Open']
    data['Volatility'] = data['High'] - data['Low']
    data = data.fillna(0)

    stock_data = data

    x = stock_data[['MA5', 'MA10', 'Price_Change', 'Volatility', 'Volume']]
    y = stock_data['open_price']
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    model = LogisticRegression()
    model.fit(x_train, y_train)

    #y_pred = model.predict(x_test)

    return model