import tkinter as tk
from tkinter import ttk
from .base_chart import BaseChartView
import matplotlib.pyplot as plt
import seaborn as sns

class Histogram(BaseChartView):
    def __init__(self, parent, df):
        super().__init__(parent, df, "Histogram")
        if self.df is not None and not self.df.empty:
            num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
            if not num_cols:
                self._show_missing_feature_msg("This dataset has no numeric columns for Histogram.")
                return
            
            self.initial_state = {"column": num_cols[0], "bins": 10}
            self._add_controls()
            self.update_chart()

    def _add_controls(self):
        num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        
        # Column
        tk.Label(self.controls_frame, text="Column:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        self.column_var = tk.StringVar(value=self.initial_state["column"])
        col_cb = ttk.Combobox(self.controls_frame, textvariable=self.column_var, values=num_cols, state="readonly")
        col_cb.pack(side=tk.LEFT, padx=5)
        col_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        # Bins
        tk.Label(self.controls_frame, text="Bins:".title(), bg="white").pack(side=tk.LEFT, padx=(15, 5))
        self.bin_var = tk.IntVar(value=self.initial_state["bins"])
        bin_slider = tk.Scale(self.controls_frame, from_=5, to=30, orient=tk.HORIZONTAL, 
                              variable=self.bin_var, bg="white", bd=0, highlightthickness=0)
        bin_slider.pack(side=tk.LEFT, padx=5)
        bin_slider.bind("<ButtonRelease-1>", lambda e: self.update_chart())

    def update_chart(self):
        self.ax.clear()
        col = self.column_var.get()
        bins = self.bin_var.get()

        sns.histplot(data=self.df, x=col, bins=bins, ax=self.ax, kde=True, color="#2ECC71")
        self.ax.set_title(f"Histogram — Distribution of {col.capitalize()}".title())
        self.ax.set_xlabel(col.title())
        self.ax.set_ylabel("Frequency".title())
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def reset_to_default(self):
        self.column_var.set(self.initial_state["column"])
        self.bin_var.set(self.initial_state["bins"])
        self.update_chart()
