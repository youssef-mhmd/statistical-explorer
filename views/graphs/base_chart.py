import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns

class CustomToolbar(NavigationToolbar2Tk):
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0] != 'Subplots']

class BaseChartView(tk.Frame):
    def __init__(self, parent, df, title):
        super().__init__(parent, bg="white")
        self.df = df
        self.title_text = title.title()
        
        sns.set_theme(style="whitegrid")
        
        if self.df is None or self.df.empty:
            self._setup_empty_state()
        else:
            self._setup_controls()
            self._setup_canvas()

    def _setup_empty_state(self):
        container = tk.Frame(self, bg="white")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(container, text="📊 No Dataset Loaded", bg="white", font=("Helvetica", 16, "bold"), fg="#2C3E50").pack(pady=(40, 10))
        tk.Label(container, text=f"The {self.title_text} requires a dataset to be loaded.\nPlease load a file first.", bg="white", font=("Helvetica", 10), fg="#95A5A6").pack()

    def _show_missing_feature_msg(self, msg):
        for widget in self.controls_frame.winfo_children():
            if widget != self.save_btn: widget.destroy()
        
        lbl = tk.Label(self.controls_frame, text=msg, fg="#E74C3C", bg="white", font=("Helvetica", 10, "italic"))
        lbl.pack(side=tk.LEFT, padx=10)
        
        self.ax.clear()
        self.ax.text(0.5, 0.5, msg, ha='center', va='center', color="#E74C3C")
        self.canvas.draw()

    def _setup_controls(self):
        self.controls_frame = tk.Frame(self, bg="white", pady=10)
        self.controls_frame.pack(fill=tk.X, padx=10)
        
        # Save Button
        self.save_btn = tk.Button(self.controls_frame, text="💾 Save As PNG".title(), command=self._save_chart,
                                  bg="#27AE60", fg="white", padx=15, font=("Helvetica", 9, "bold"), bd=0, cursor="hand2")
        self.save_btn.pack(side=tk.RIGHT, padx=10)

        # Reset Button (Hidden by default, used by subclasses)
        self.reset_btn = tk.Button(self.controls_frame, text="🔄 Reset To Default".title(), command=self.reset_to_default,
                                   bg="#E74C3C", fg="white", padx=15, font=("Helvetica", 9, "bold"), bd=0, cursor="hand2")

    def _setup_canvas(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        self.toolbar = CustomToolbar(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _save_chart(self):
        suggested_name = self.title_text.replace(" ", "_") + ".png"
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 initialfile=suggested_name,
                                                 filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path:
            try:
                self.fig.savefig(file_path)
                messagebox.showinfo("Success".title(), f"Chart Saved To {file_path}".title())
            except Exception as e:
                messagebox.showerror("Error".title(), f"Failed To Save Chart: {e}".title())

    def reset_to_default(self):
        # To be implemented by subclasses
        pass
