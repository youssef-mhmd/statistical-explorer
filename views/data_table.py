import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataTable(tk.Frame):
    def __init__(self, parent, df):
        super().__init__(parent, bg="#F8F9FA")
        self.df = df
        
        if self.df is None or self.df.empty:
            self._setup_empty_state()
            return

        self._setup_ui()
        self._load_data()

    def _setup_empty_state(self):
        container = tk.Frame(self, bg="white", bd=1, relief=tk.RIDGE)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=200)
        tk.Label(container, text="📋 No Dataset Loaded", bg="white", font=("Helvetica", 16, "bold"), fg="#2C3E50").pack(pady=(40, 10))
        tk.Label(container, text="The dataset 'mid term grades.csv' could not be found.", bg="white", font=("Helvetica", 10), fg="#95A5A6").pack()

    def _setup_ui(self):
        # Header Info
        self.info_frame = tk.Frame(self, bg="#F8F9FA")
        self.info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        count = len(self.df)
        limit = 200
        msg = f"📊 Total Records: {count} | Showing first {min(count, limit)} for maximum speed."
        tk.Label(self.info_frame, text=msg, bg="#F8F9FA", fg="#7F8C8D", font=("Helvetica", 10, "italic")).pack(side=tk.LEFT)

        # Table Container
        table_container = tk.Frame(self, bg="white", bd=1, relief=tk.RIDGE)
        table_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        cols = list(self.df.columns)
        self.tree = ttk.Treeview(table_container, columns=cols, show='headings', selectmode="browse")
        
        # Optimize column setup
        for col in cols:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=100, anchor=tk.CENTER)

        sy = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        sx = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=sy.set, xscroll=sx.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        sy.grid(row=0, column=1, sticky='ns')
        sx.grid(row=1, column=0, sticky='ew')
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

    def _load_data(self):
        # Faster loading: limit to 200 rows for large datasets
        limit = 200
        display_df = self.df.head(limit)
        
        # Convert entire slice to string list at once for speed
        rows = display_df.fillna("—").values.tolist()
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)
