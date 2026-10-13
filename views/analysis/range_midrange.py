import pandas as pd
import seaborn as sns
import tkinter as tk
from .base_analysis import BaseAnalysisView

class RangeMidRange(BaseAnalysisView):
    def __init__(self, parent, df):
        formula = "Range = Max - Min | MidRange = (Max+Min)/2"
        super().__init__(parent, df, "Range & Mid Range", formula)
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()

    def calculate_and_display(self):
        numeric_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        if not numeric_cols:
            tk.Label(self.table_frame, text="No numeric columns found.", fg="red", bg="white").pack()
            return

        results = []
        for col in numeric_cols:
            c_max = self.df[col].max()
            c_min = self.df[col].min()
            results.append({
                "Column": col.upper(),
                "Range": round(float(c_max - c_min), 2),
                "Mid Range": round(float((c_max + c_min) / 2), 2)
            })

        res_df = pd.DataFrame(results)
        self.update_table(res_df)

        self.ax.clear()
        # Horizontal representation (y=Column) prevents label overlapping
        melted = res_df.melt(id_vars="Column", var_name="Measure", value_name="Value")
        sns.barplot(data=melted, y="Column", x="Value", hue="Measure", ax=self.ax, palette="Oranges")
        
        self.ax.set_title("Range & Mid-Range Comparison".title())
        self.ax.set_xlabel("Value")
        self.ax.set_ylabel("") # Column names are already clear
        
        self.fig.tight_layout()
        self.canvas.draw()

    def reset_to_default(self):
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()
