import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import datetime as dt
import yfinance as yf


def train_regression_model(csv):
        data = pd.read_csv(csv)
        
        # Calculates the change in price between the current and the previous element
        data['price_change'] = data['close'].pct_change()

        # Add the value if its greater then 0 if it was convert it to a bool value
        data['label'] = (data['price_change'] > 0).astype(int)

        X = data[['open', 'high', 'low', 'close', 'volume']]
        y = data['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = r2_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}') 
        return model