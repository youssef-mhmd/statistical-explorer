import tkinter as tk
from tkinter import ttk
from .base_chart import BaseChartView
import seaborn as sns

class BarPlot(BaseChartView):
    def __init__(self, parent, df):
        super().__init__(parent, df, "Bar Plot")
        self.initial_state = {"group": "college", "y_axis": "Count"}
        self._add_controls()
        self.update_chart()

    def _add_controls(self):
        # Group By
        tk.Label(self.controls_frame, text="Group By:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        
        cat_cols = [col for col in self.df.columns if self.df[col].dtype == 'category' or self.df[col].dtype == 'object' or self.df[col].nunique() < 15]
        if not cat_cols:
            self._show_missing_feature_msg("This dataset doesn't have suitable categorical columns for a Bar Plot.")
            return
        
        if self.initial_state["group"] not in cat_cols:
            self.initial_state["group"] = cat_cols[0]

        self.group_var = tk.StringVar(value=self.initial_state["group"])
        group_cb = ttk.Combobox(self.controls_frame, textvariable=self.group_var, 
                                values=cat_cols, state="readonly")
        group_cb.pack(side=tk.LEFT, padx=5)
        group_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

        # Y-Axis
        tk.Label(self.controls_frame, text="Y-Axis:".title(), bg="white").pack(side=tk.LEFT, padx=5)
        
        y_options = ["Count"]
        num_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'int64']]
        for col in num_cols:
            y_options.append(f"Mean {col}")
            
        self.y_var = tk.StringVar(value=self.initial_state["y_axis"])
        y_cb = ttk.Combobox(self.controls_frame, textvariable=self.y_var, values=y_options, state="readonly")
        y_cb.pack(side=tk.LEFT, padx=5)
        y_cb.bind("<<ComboboxSelected>>", lambda e: self.update_chart())

    def _show_missing_feature_msg(self, msg):
        for widget in self.controls_frame.winfo_children():
            if widget != self.save_btn: widget.destroy()
        
        lbl = tk.Label(self.controls_frame, text=msg, fg="#E74C3C", bg="white", font=("Helvetica", 10, "italic"))
        lbl.pack(side=tk.LEFT, padx=10)
        
        self.ax.clear()
        self.ax.text(0.5, 0.5, msg, ha='center', va='center', color="#E74C3C")
        self.canvas.draw()

    def reset_to_default(self):
        self.group_var.set(self.initial_state["group"])
        self.y_var.set(self.initial_state["y_axis"])
        self.update_chart()

    def update_chart(self):
        self.ax.clear()
        if self.df.empty:
            self.ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
            self.canvas.draw()
            return

        group_col = self.group_var.get()
        y_type = self.y_var.get()

        try:
            if y_type == "Count":
                sns.countplot(data=self.df, x=group_col, ax=self.ax, palette="viridis")
                self.ax.set_ylabel("Count")
            elif y_type.startswith("Mean "):
                col = y_type.replace("Mean ", "")
                sns.barplot(data=self.df, x=group_col, y=col, ax=self.ax, palette="magma")
                self.ax.set_ylabel(f"Mean {col}")

            self.ax.set_title(f"Bar Plot — {y_type} By {group_col.capitalize()}".title())
            self.ax.set_xlabel(group_col.title())
            
            for p in self.ax.patches:
                val = f'{p.get_height():.2f}' if y_type != "Count" else f'{int(p.get_height())}'
                self.ax.annotate(val, (p.get_x() + p.get_width() / 2., p.get_height()), 
                                 ha='center', va='center', fontsize=10, xytext=(0, 5),
                                 textcoords='offset points')
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error plotting: {e}", ha='center', va='center')

        self.fig.tight_layout()
        self.canvas.draw()
        
        is_modified = (self.group_var.get() != self.initial_state["group"] or 
                       self.y_var.get() != self.initial_state["y_axis"])
        if is_modified: self.reset_btn.pack(side=tk.RIGHT, padx=10)
        else: self.reset_btn.pack_forget()
