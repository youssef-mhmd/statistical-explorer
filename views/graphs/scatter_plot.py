import tkinter as tk
from tkinter import ttk
from .base_chart import BaseChartView
import seaborn as sns

class ScatterPlot(BaseChartView):
    def __init__(self, parent, df):
        super().__init__(parent, df, "Scatter Plot")
        if self.df is not None and not self.df.empty:
            num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
            if len(num_cols) < 2:
                self._show_missing_feature_msg("This dataset needs at least 2 numeric columns for Scatter Plot.")
                return
            
            cat_cols = [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]
            
            self.initial_state = {
                "x": num_cols[0], 
                "y": num_cols[1], 
                "hue": cat_cols[0] if cat_cols else "None"
            }
            self._add_controls()
            self.update_chart()

    def _add_controls(self):
        num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        cat_cols = ["None"] + [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]

        # X-Axis
        tk.Label(self.controls_frame, text="X-Axis:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        self.x_var = tk.StringVar(value=self.initial_state["x"])
        x_cb = ttk.Combobox(self.controls_frame, textvariable=self.x_var, values=num_cols, state="readonly", width=12)
        x_cb.pack(side=tk.LEFT, padx=5)
        x_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        # Y-Axis
        tk.Label(self.controls_frame, text="Y-Axis:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        self.y_var = tk.StringVar(value=self.initial_state["y"])
        y_cb = ttk.Combobox(self.controls_frame, textvariable=self.y_var, values=num_cols, state="readonly", width=12)
        y_cb.pack(side=tk.LEFT, padx=5)
        y_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        # Hue
        tk.Label(self.controls_frame, text="Color By:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        self.hue_var = tk.StringVar(value=self.initial_state["hue"])
        hue_cb = ttk.Combobox(self.controls_frame, textvariable=self.hue_var, values=cat_cols, state="readonly", width=12)
        hue_cb.pack(side=tk.LEFT, padx=5)
        hue_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

    def update_chart(self):
        self.ax.clear()
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        hue_col = self.hue_var.get()
        if hue_col == "None": hue_col = None

        sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=hue_col, ax=self.ax, palette="viridis", s=100)
        self.ax.set_title(f"Scatter Plot — {x_col.title()} vs {y_col.title()}".title())
        self.ax.set_xlabel(x_col.title())
        self.ax.set_ylabel(y_col.title())
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def reset_to_default(self):
        self.x_var.set(self.initial_state["x"])
        self.y_var.set(self.initial_state["y"])
        self.hue_var.set(self.initial_state["hue"])
        self.update_chart()
