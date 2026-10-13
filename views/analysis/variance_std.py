import pandas as pd
import seaborn as sns
import tkinter as tk
from .base_analysis import BaseAnalysisView

class VarianceStdDev(BaseAnalysisView):
    def __init__(self, parent, df):
        formula = "Var = Σ(x-μ)²/n | Std Dev = √Var"
        super().__init__(parent, df, "Variance & Std Dev", formula)
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()

    def calculate_and_display(self):
        numeric_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        if not numeric_cols:
            tk.Label(self.table_frame, text="No numeric columns found.", fg="red", bg="white").pack()
            return

        results = []
        for col in numeric_cols:
            results.append({
                "Column": col.upper(),
                "Variance": round(self.df[col].var(), 2),
                "Std Dev": round(self.df[col].std(), 2)
            })

        res_df = pd.DataFrame(results)
        self.update_table(res_df)

        self.ax.clear()
        melted = res_df.melt(id_vars="Column", var_name="Measure", value_name="Value")
        sns.barplot(data=melted, x="Value", y="Column", hue="Measure", ax=self.ax, palette="magma")
        self.ax.set_title("Variance Vs Standard Deviation".title())
        self.fig.tight_layout()
        self.canvas.draw()

    def reset_to_default(self):
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()
