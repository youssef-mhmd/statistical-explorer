import tkinter as tk
from tkinter import ttk
from .base_chart import BaseChartView
import seaborn as sns

class BoxPlot(BaseChartView):
    def __init__(self, parent, df):
        super().__init__(parent, df, "Box Plot")
        if self.df is not None and not self.df.empty:
            num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
            if not num_cols:
                self._show_missing_feature_msg("This dataset has no numeric columns for Box Plot.")
                return
            
            cat_cols = [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]
            
            self.initial_state = {
                "column": num_cols[0], 
                "group": cat_cols[0] if cat_cols else "None"
            }
            self._add_controls()
            self.update_chart()

    def _add_controls(self):
        num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        cat_cols = ["None"] + [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]

        # Column
        tk.Label(self.controls_frame, text="Column:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        self.column_var = tk.StringVar(value=self.initial_state["column"])
        col_cb = ttk.Combobox(self.controls_frame, textvariable=self.column_var, values=num_cols, state="readonly")
        col_cb.pack(side=tk.LEFT, padx=5)
        col_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        # Group By
        tk.Label(self.controls_frame, text="Group By:".title(), bg="white").pack(side=tk.LEFT, padx=(15, 5))
        self.group_var = tk.StringVar(value=self.initial_state["group"])
        group_cb = ttk.Combobox(self.controls_frame, textvariable=self.group_var, values=cat_cols, state="readonly")
        group_cb.pack(side=tk.LEFT, padx=5)
        group_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

    def update_chart(self):
        self.ax.clear()
        col = self.column_var.get()
        group = self.group_var.get()
        if group == "None": group = None

        sns.boxplot(data=self.df, y=col, x=group, ax=self.ax, palette="Set2")
        self.ax.set_title(f"Box Plot — {col.capitalize()} By {str(group).capitalize() if group else 'All'}".title())
        self.ax.set_ylabel(col.title())
        if group: self.ax.set_xlabel(group.title())
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def reset_to_default(self):
        self.column_var.set(self.initial_state["column"])
        self.group_var.set(self.initial_state["group"])
        self.update_chart()
