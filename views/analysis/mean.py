import pandas as pd
import seaborn as sns
import tkinter as tk
from .base_analysis import BaseAnalysisView

class Mean(BaseAnalysisView):
    def __init__(self, parent, df):
        formula = "Mean = Σx / n"
        super().__init__(parent, df, "Mean (Average)", formula)
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()

    def calculate_and_display(self):
        numeric_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        if not numeric_cols:
            tk.Label(self.table_frame, text="No numeric columns found.", fg="red", bg="white").pack()
            return
            
        results = []
        for col in numeric_cols:
            results.append({"Column": col.upper(), "Mean": round(self.df[col].mean(), 2)})

        res_df = pd.DataFrame(results).sort_values(by="Mean", ascending=False)
        self.update_table(res_df)

        self.ax.clear()
        sns.barplot(data=res_df, y="Column", x="Mean", ax=self.ax, palette="YlGnBu")
        self.ax.set_title("Mean Values (Sorted)".title())
        for i, p in enumerate(self.ax.patches):
            self.ax.annotate(f'{p.get_width():.2f}', (p.get_width(), i), 
                             ha='left', va='center', fontsize=10, xytext=(5, 0),
                             textcoords='offset points')
        self.fig.tight_layout()
        self.canvas.draw()
        
    def reset_to_default(self):
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()
