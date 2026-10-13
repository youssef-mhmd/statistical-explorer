import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class BaseAnalysisView(tk.Frame):
    def __init__(self, parent, df, title, formula):
        super().__init__(parent, bg="white")
        self.df = df
        
        sns.set_theme(style="whitegrid")

        if self.df is None or self.df.empty:
            self._setup_empty_state(title)
            return

        # Top Bar (Formula + Reset)
        self.top_bar = tk.Frame(self, bg="#ECF0F1", pady=10)
        self.top_bar.pack(fill=tk.X, padx=10, pady=5)
        
        self.formula_label = tk.Label(self.top_bar, text=f"Formula: {formula}".title(), font=("Courier", 11, "bold"), 
                                      bg="#ECF0F1", fg="#2C3E50")
        self.formula_label.pack(side=tk.LEFT, padx=15)

        self.reset_btn = tk.Button(self.top_bar, text="🔄 Reset".title(), command=self.reset_to_default,
                                   bg="#E74C3C", fg="white", font=("Helvetica", 9, "bold"), bd=0, padx=15, cursor="hand2")

        # Split into Table and Chart
        self.main_split = tk.Frame(self, bg="white")
        self.main_split.pack(fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.main_split, bg="white", width=400)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.chart_frame = tk.Frame(self.main_split, bg="white")
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._setup_table()
        self._setup_chart()

    def _setup_empty_state(self, title):
        container = tk.Frame(self, bg="white")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(container, text="🔢 No Dataset Loaded", bg="white", font=("Helvetica", 16, "bold"), fg="#2C3E50").pack(pady=(40, 10))
        tk.Label(container, text=f"The {title} analysis requires a dataset to be loaded.\nPlease load a file first.", bg="white", font=("Helvetica", 10), fg="#95A5A6").pack()

    def _setup_table(self):
        pass

    def _setup_chart(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_table(self, data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        cols = list(data.columns)
        tree = ttk.Treeview(self.table_frame, columns=cols, show='headings', height=10)
        
        for col in cols:
            tree.heading(col, text=col.title())
            tree.column(col, width=120, anchor=tk.CENTER)
        
        for _, row in data.iterrows():
            values = [str(v).title() for v in row]
            tree.insert("", tk.END, values=values)
        tree.pack(fill=tk.BOTH, expand=True)

    def reset_to_default(self):
        pass
