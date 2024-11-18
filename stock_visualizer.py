import tkinter as tk
from tkinter import ttk

from matplotlib import pyplot as plt
import pandas as pd

class StockVisualizerApp:
    def __init__(self, root, df, ticker):
        self.root = root
        self.df = df
        self.ticker = ticker
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text=f"Visualizing {self.ticker}").pack()

        if isinstance(self.df, pd.DataFrame) and "high" in self.df.columns:
            ax = plt.subplots(1, 1, figsize=(6, 8), layout='constrained')

# Example usage if needed
if __name__ == "__main__":
    root = tk.Tk()
    df = None  # Replace with your DataFrame
    ticker = "AAPL"  # Replace with your ticker
    StockVisualizerApp(root, df, ticker)
    root.mainloop()