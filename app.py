import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from parser import parse_dataset

# Import views
from views.data_table import DataTable
from views.graphs.bar_plot import BarPlot
from views.graphs.scatter_plot import ScatterPlot
from views.graphs.histogram import Histogram
from views.graphs.box_plot import BoxPlot
from views.graphs.pie_chart import PieChart
from views.analysis.range_midrange import RangeMidRange
from views.analysis.mean import Mean
from views.analysis.median import Median
from views.analysis.mode import Mode
from views.analysis.variance_std import VarianceStdDev

class StatsExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.theme = {
            "bg": "#F8F9FA",
            "header_bg": "#1A252F",
            "sidebar_bg": "#2C3E50",
            "sidebar_hover": "#34495E",
            "accent": "#3498DB",
            "text": "#2C3E50",
            "subtext": "#95A5A6",
            "card_bg": "white",
            "border": "#ECF0F1"
        }

        self.title("Statistical Explorer")
        self.geometry("1250x850")
        
        self.df = None
        self.current_view_name = None
        self.current_view_widget = None
        self.sidebar_buttons = {}
        
        self._setup_ui()
        self._autoload_dataset()
        self.show_view("Data Table")

    def _autoload_dataset(self):
        import os
        file_path = "mid term grades.csv"
        if os.path.exists(file_path):
            try:
                self.df = pd.read_csv(file_path)
                self._after_data_load(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to autoload '{file_path}': {e}")

    def _setup_ui(self):
        self.configure(bg=self.theme["bg"])
        
        # Header
        self.header = tk.Frame(self, bg=self.theme["header_bg"], height=70)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        self.title_label = tk.Label(self.header, text="Statistical Explorer", 
                                    fg="white", bg=self.theme["header_bg"], font=("Helvetica", 18, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=25, pady=20)

        self.info_label = tk.Label(self.header, text="No Dataset Loaded", 
                              fg=self.theme["subtext"], bg=self.theme["header_bg"], font=("Helvetica", 10))
        self.info_label.pack(side=tk.RIGHT, padx=15, pady=25)

        self.main_container = tk.Frame(self, bg=self.theme["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_container, bg=self.theme["sidebar_bg"], width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self._setup_sidebar()

        self.content_area = tk.Frame(self.main_container, bg=self.theme["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self, textvariable=self.status_var, bd=0, relief=tk.FLAT, 
                                   anchor=tk.W, bg=self.theme["border"], fg=self.theme["subtext"], padx=10, pady=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _setup_sidebar(self):
        sections = [
            ("📋 Data", ["Data Table"]),
            ("📊 Graphs", ["Bar Plot", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart"]),
            ("🔢 Analysis", ["Range & Mid Range", "Mean", "Median", "Mode", "Variance & Std Dev"])
        ]

        for section_title, items in sections:
            tk.Label(self.sidebar, text=section_title, bg=self.theme["header_bg"], fg=self.theme["subtext"], 
                     font=("Helvetica", 9, "bold"), pady=10, anchor="w", padx=15).pack(fill=tk.X)
            
            for item in items:
                btn = tk.Button(self.sidebar, text=item, bg=self.theme["sidebar_bg"], fg="white", 
                                activebackground=self.theme["accent"], activeforeground="white",
                                bd=0, padx=25, pady=10, anchor="w", cursor="hand2",
                                font=("Helvetica", 10),
                                command=lambda i=item: self.show_view(i))
                btn.pack(fill=tk.X)
                self.sidebar_buttons[item] = btn
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.theme["sidebar_hover"]))
                btn.bind("<Leave>", lambda e, b=btn, i=item: self._on_leave(b, i))

    def _on_leave(self, btn, item):
        if item != self.current_view_name:
            btn.configure(bg=self.theme["sidebar_bg"])

    def _after_data_load(self, source_name):
        self.info_label.configure(text=f"Source: {source_name} | Records: {len(self.df)}")
        self.current_view_name = None 
        self.show_view("Data Table")

    def show_view(self, view_name):
        if view_name == self.current_view_name: return
        if self.current_view_name in self.sidebar_buttons:
            self.sidebar_buttons[self.current_view_name].configure(bg=self.theme["sidebar_bg"])
        
        self.current_view_name = view_name
        if view_name in self.sidebar_buttons:
            self.sidebar_buttons[view_name].configure(bg=self.theme["accent"])

        if self.current_view_widget: self.current_view_widget.destroy()

        view_map = {
            "Data Table": DataTable, "Bar Plot": BarPlot, "Scatter Plot": ScatterPlot,
            "Histogram": Histogram, "Box Plot": BoxPlot, "Pie Chart": PieChart,
            "Range & Mid Range": RangeMidRange, "Mean": Mean, "Median": Median,
            "Mode": Mode, "Variance & Std Dev": VarianceStdDev
        }

        if view_name in view_map:
            self.current_view_widget = view_map[view_name](self.content_area, self.df)
            self.current_view_widget.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = StatsExplorerApp()
    app.mainloop()
