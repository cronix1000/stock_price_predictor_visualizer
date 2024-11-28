import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import yfinance as yf

from stock_data_ai import train_regression_model  
from real_time_stock_price import real_time_price
from predict_price import predict_price_movement

class StockTickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Data Fetcher")
        self.root.geometry("800x200")
        
        self.default_tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META',
            'NVDA', 'TSLA', 'JPM', 'V', 'WMT'
        ]
        
        self.create_widgets()

    def create_widgets(self):
        self.main_widgets = []

        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill="both", expand=True)
        self.main_widgets.append(content_frame)
        
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ttk.Label(left_frame, text="Available Tickers").pack()
        self.ticker_listbox = tk.Listbox(left_frame, selectmode="extended")
        self.ticker_listbox.pack(fill="both", expand=True)
        
        for ticker in self.default_tickers:
            self.ticker_listbox.insert(tk.END, ticker)
        
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", pady=5)
        
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        ttk.Label(right_frame, text="Input Date (YYYY-MM-DD):").pack()
        self.date_entry = ttk.Entry(right_frame)
        self.date_entry.pack(pady=5)
    
        ttk.Button(right_frame, text="Get Data", command=self.fetch_data).pack(pady=10)


    def fetch_data(self):
        selection = self.ticker_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select at least one ticker!")
            return
        
        selected_tickers = [self.ticker_listbox.get(i) for i in selection]
        input_date = self.date_entry.get().strip()

        

        try:
            target_date = datetime.strptime(input_date, "%Y-%m-%d")
            start_date = (target_date - timedelta(days=30)).strftime("%Y-%m-%d")
            end_date = target_date.strftime("%Y-%m-%d")

            print(target_date, start_date, end_date)

            for ticker in selected_tickers:
                # Download data
                data = yf.download(ticker, start=start_date, end=end_date)
                if data.empty:
                    messagebox.showerror("Error", f"No data found for {ticker}.")
                    continue

                data['open_price'] = (data['Open'].shift(-1) > data['Open']).astype(int)
                data = data.dropna()

                # Train model
                model = train_regression_model(data)

                # Prepare features
                features = data[['Open', 'High', 'Low', 'Close', 'Volume']].iloc[-1].values.reshape(1, -1)
                prediction = predict_price_movement(model, features)
                actual_direction = data['open_price'].iloc[-1]
                print(f"Prediction: {prediction}, Actual: {actual_direction}")

                messagebox.showinfo(f"Prediction Result: {0}, Actual Result {1}", prediction, actual_direction)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StockTickerApp(root)
    root.mainloop()

