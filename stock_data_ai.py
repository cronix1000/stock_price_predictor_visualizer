import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import datetime as dt
import yfinance as yf
from textblob import TextBlob
from datetime import datetime

def train_regression_model(csv, symbol):
        data = csv
        
        sentiment_data = get_news_sentiment(symbol,symbol)

        data['date'] = pd.to_datetime(data.index)
        merged_data = pd.merge(data, sentiment_data, on='date', how='left')
        merged_data['sentiment'] = merged_data['sentiment'].fillna(0)

        # Calculates the change in price between the current and the previous element
        data['price_change'] = data['close'].pct_change()

        # Add the value if its greater then 0 if it was convert it to a bool value
        data['label'] = (data['price_change'] > 0).astype(int)



        X = data[['open', 'high', 'low', 'close', 'volume']]
        y = data['label']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        accuracy = r2_score(y_test, y_pred)
        
        return model, accuracy, merged_data



def get_news_sentiment(self, symbol, days=30):
        """Fetch news and calculate sentiment scores for the stock."""
        try:
            stock = yf.Ticker(symbol)
            news = stock.news
            
            sentiments = []
            dates = []
            
            for article in news:
                if 'title' in article:
                    blob = TextBlob(article['title'])
                    sentiment = blob.sentiment.polarity
                    date = datetime.fromtimestamp(article['providerPublishTime'])
                    sentiments.append(sentiment)
                    dates.append(date)
            
            return pd.DataFrame({
                'date': dates,
                'sentiment': sentiments
            })
        except Exception as e:
            print(f"Error fetching news: {e}")
            return pd.DataFrame(columns=['date', 'sentiment'])

