import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from real_time_stock_price import real_time_price

class StockVisualizerApp:
    def __init__(self, root, ticker, prediction, price_at_prediction):
        self.root = root
        self.prediction = prediction
        self.price_at_prediction = price_at_prediction
        self.ticker = ticker
        self.setup_ui()


    def setup_ui(self):
        self.control_frame = ttk.Frame(self.root, padding="5")
        self.control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))       
        title_label = ttk.Label(self.control_frame, 
                               text=f"Stock Analysis for {self.ticker}",
                               font=('Helvetica', 12, 'bold'))
        title_label.grid(row=0, column=0, pady=5)

        self.price_label = ttk.Label(self.control_frame, text="Current Price: N/A")
        self.price_label.grid(row=2, column=0, pady=5)

        self.count_down_label = ttk.Label(self.control_frame, text="Countdown: 60")
        self.count_down_label.grid(row=3, column=0, pady=5)

        self.price_prediction_result_label = ttk.Label(self.control_frame, "The prediction was...")



        self.start_countdown()

    def start_countdown(self):
        self.remaining_time = 60
        self.update_countdown()         

    def update_countdown(self):
        if self.remaining_time > 0:
            self.count_down_label.config(text=f"Countdown: {self.remaining_time}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.count_down_label.config(text="Countdown: 0")
            self.check_current_price()

    def check_current_price(self):
        self.current_price = real_time_price(self.ticker)
        self.price_label.config(text=f"Current Price: {self.current_price}")
        result = 'up'

        if self.price_at_prediction <= self.current_price:
            result = 'down'
        else:
            result = 'up'

        self.price_prediction_result_label.config(text=f"Prediction Result: {result}")
        return result




        
if __name__ == "__main__":
    root = tk.Tk()