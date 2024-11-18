import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pandas as pd
from datetime import datetime
import json

from stock_data_ai import train_regression_model  
from real_time_stock_price import real_time_price
from predict_price import predict_price_movement
from stock_visualizer import StockVisualizerApp

class StockTickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Data Fetcher")
        self.root.geometry("800x600")
        self.api_key = self.load_api_key()
        
        self.default_tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META',
            'NVDA', 'TSLA', 'JPM', 'V', 'WMT'
        ]
        
        self.create_widgets()
    
    def load_api_key(self):
            with open('secrets.json', 'r') as file:
                secrets = json.load(file)
                return secrets.get('alpha_vantage_api_key', '')

    def create_widgets(self):
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill="both", expand=True)
        
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ttk.Label(left_frame, text="Available Tickers").pack()
        self.ticker_listbox = tk.Listbox(left_frame, selectmode="extended")
        self.ticker_listbox.pack(fill="both", expand=True)
        
        for ticker in self.default_tickers:
            self.ticker_listbox.insert(tk.END, ticker)
        
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="Add Ticker", command=self.add_ticker).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_ticker).pack(side="left", padx=2)
        
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ttk.Label(right_frame, text="Interval:").pack()
        self.interval_var = tk.StringVar(value="5min")
        interval_frame = ttk.Frame(right_frame)
        interval_frame.pack(fill="x")
        
        intervals = [("1min", "1min"), ("5min", "5min"), ("15min", "15min"), ("30min", "30min"), ("60min", "60min")]
        for text, value in intervals:
            ttk.Radiobutton(interval_frame, text=text, value=value, variable=self.interval_var).pack(side="left")
        
        # Fetch Button
        ttk.Button(right_frame, text="Get Data", command=self.fetch_data).pack(pady=10)
        
        # Status Frame
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=5)
   
    def add_ticker(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Ticker")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="Enter Ticker Symbol:").pack(pady=5)
        entry = ttk.Entry(dialog)
        entry.pack(pady=5)
        
        def submit():
            ticker = entry.get().strip().upper()
            if ticker:
                self.ticker_listbox.insert(tk.END, ticker)
                dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=submit).pack(pady=5)
        
    def remove_ticker(self):
        selection = self.ticker_listbox.curselection()
        for index in reversed(selection):
            self.ticker_listbox.delete(index)
        
    def fetch_data(self):
        if not self.api_key:
            messagebox.showerror("Error", "Please enter an API key first!")
            return
            
        selection = self.ticker_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select at least one ticker!")
            return
            
        selected_tickers = [self.ticker_listbox.get(i) for i in selection]
        interval = self.interval_var.get()
        
        for ticker in selected_tickers:
            self.status_var.set(f"Fetching data for {ticker}...")
            self.root.update()
            
            try:
                url = (f"https://www.alphavantage.co/query?"
                      f"function=TIME_SERIES_INTRADAY"
                      f"&symbol={ticker}"
                      f"&interval={interval}"
                      f"&apikey={self.api_key}"
                      f"&outputsize=full")
                
                response = requests.get(url)
                data = response.json()
                

                
                if "Error Message" in data:
                    messagebox.showerror("Error", f"Error fetching {ticker}: {data['Error Message']}")
                    continue

                time_series_key = f"Time Series ({interval})"
                if time_series_key not in data:
                    messagebox.showerror("Error", f"No data available for {ticker}")
                    continue
                    
                df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
        
                df.columns = ['open', 'high', 'low', 'close', 'volume']
                
                df.index = pd.to_datetime(df.index)
                
                df.sort_index(inplace=True)
                
                filename = f"{ticker}_{interval}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename)
                messagebox.showinfo("Success", f"Data for {ticker} saved to {filename}")

                features = df[df.columns].iloc[-1].values.reshape(1, -1)
                print(features)

                model = train_regression_model(filename)
                current_price = real_time_price(ticker)
                pred = predict_price_movement(model, current_price, features)
                print(pred)

                for widget in self.root.winfo_children():
                    widget.destroy()

                StockVisualizerApp(self.root, df, ticker)


                
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {ticker}: {str(e)}")
            
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTickerApp(root)
    root.mainloop()

