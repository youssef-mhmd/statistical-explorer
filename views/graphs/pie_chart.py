import tkinter as tk
from tkinter import ttk
from .base_chart import BaseChartView
import matplotlib.pyplot as plt

class PieChart(BaseChartView):
    def __init__(self, parent, df):
        super().__init__(parent, df, "Pie Chart")
        if self.df is not None and not self.df.empty:
            self.initial_state = {"column": None}
            self._add_controls()
            self.update_chart()

    def _add_controls(self):
        # Select Column
        tk.Label(self.controls_frame, text="Select Column:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        
        # Find categorical columns or those with low cardinality
        cat_cols = [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]
        
        if not cat_cols:
            self._show_missing_feature_msg("This dataset doesn't have suitable categorical columns for a Pie Chart.")
            return

        self.initial_state["column"] = cat_cols[0]
        self.column_var = tk.StringVar(value=self.initial_state["column"])
        column_cb = ttk.Combobox(self.controls_frame, textvariable=self.column_var, 
                                 values=cat_cols, state="readonly")
        column_cb.pack(side=tk.LEFT, padx=5)
        column_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

    def _show_missing_feature_msg(self, msg):
        for widget in self.controls_frame.winfo_children():
            if widget != self.save_btn: widget.destroy()
        
        lbl = tk.Label(self.controls_frame, text=msg, fg="#E74C3C", bg="white", font=("Helvetica", 10, "italic"))
        lbl.pack(side=tk.LEFT, padx=10)
        
        self.ax.clear()
        self.ax.text(0.5, 0.5, msg, ha='center', va='center', color="#E74C3C")
        self.canvas.draw()

    def reset_to_default(self):
        self.column_var.set(self.initial_state["column"])
        self.update_chart()

    def update_chart(self):
        self.ax.clear()
        if self.df.empty:
            self.ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
            self.canvas.draw()
            return

        column = self.column_var.get()
        if column not in self.df.columns:
            self.ax.text(0.5, 0.5, f"Column {column} Not Found", ha='center', va='center')
            self.canvas.draw()
            return

        data = self.df[column].value_counts()
        if data.empty:
            self.ax.text(0.5, 0.5, "No Values to Plot", ha='center', va='center')
            self.canvas.draw()
            return
        
        self.ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140, 
                    colors=plt.cm.Paired.colors)
        
        self.ax.set_title(f"Pie Chart — Distribution of {column.capitalize()}".title())
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        is_modified = (self.column_var.get() != self.initial_state["column"])
        if is_modified: self.reset_btn.pack(side=tk.RIGHT, padx=10)
        else: self.reset_btn.pack_forget()
