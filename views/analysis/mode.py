import pandas as pd
import seaborn as sns
import tkinter as tk
from .base_analysis import BaseAnalysisView

class Mode(BaseAnalysisView):
    def __init__(self, parent, df):
        formula = "Mode = Value with highest frequency"
        super().__init__(parent, df, "Mode", formula)
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()

    def calculate_and_display(self):
        # Calculate mode for all columns
        results = []
        for col in self.df.columns:
            counts = self.df[col].value_counts()
            if not counts.empty:
                mode_val = counts.index[0]
                freq = counts.iloc[0]
                results.append({
                    "Column": col.title(), 
                    "Mode Value": str(mode_val), 
                    "Frequency": int(freq)
                })

        res_df = pd.DataFrame(results).sort_values(by="Frequency", ascending=False)
        self.update_table(res_df)

        # Graphical Representation
        self.ax.clear()
        
        # Pick the most interesting column to plot (the one with the highest mode frequency)
        if not res_df.empty:
            top_col_name = res_df.iloc[0]['Column'].lower()
            # If the original column was numeric, show distribution
            # If categorical, show top counts
            
            # Find the actual column in DF (case matching)
            actual_col = None
            for c in self.df.columns:
                if c.lower() == top_col_name:
                    actual_col = c
                    break
            
            if actual_col:
                data = self.df[actual_col].value_counts().head(8)
                sns.barplot(x=data.values, y=data.index.astype(str), ax=self.ax, palette="viridis")
                self.ax.set_title(f"Frequencies in '{actual_col}' (Top 8)".title())
                self.ax.set_xlabel("Count")
            else:
                # Fallback if names don't match for some reason
                sns.barplot(data=res_df.head(10), x="Frequency", y="Column", ax=self.ax, palette="magma")
                self.ax.set_title("Frequency of Modes per Column".title())
        
        self.fig.tight_layout()
        self.canvas.draw()

    def reset_to_default(self):
        if self.df is not None and not self.df.empty:
            self.calculate_and_display()
