import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from data_analyzer.core import analyze_file
from data_analyzer.report import format_report, save_report_json


class AnalyzerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Data Analytics Desktop")
        self.root.geometry("920x640")

        self.path_var = tk.StringVar()
        self.report_cache = None

        top = tk.Frame(root)
        top.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(top, text="Dataset (CSV/JSON):").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.path_var, width=80).pack(side=tk.LEFT, padx=8)
        tk.Button(top, text="Browse", command=self.browse).pack(side=tk.LEFT)

        actions = tk.Frame(root)
        actions.pack(fill=tk.X, padx=10)
        tk.Button(actions, text="Analyze", command=self.analyze).pack(side=tk.LEFT)
        tk.Button(actions, text="Save JSON Report", command=self.save_report).pack(side=tk.LEFT, padx=8)

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def browse(self):
        path = filedialog.askopenfilename(
            title="Select dataset",
            filetypes=[("Data Files", "*.csv *.json"), ("All Files", "*.*")],
        )
        if path:
            self.path_var.set(path)

    def analyze(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning("Missing file", "Choose a dataset file first.")
            return
        try:
            report = analyze_file(path)
            self.report_cache = report
            text = format_report(report)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Analyze failed", str(e))

    def save_report(self):
        if not self.report_cache:
            messagebox.showinfo("No report", "Run analysis first.")
            return
        output_path = filedialog.asksaveasfilename(
            title="Save report",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
        )
        if not output_path:
            return
        try:
            saved = save_report_json(self.report_cache, output_path)
            messagebox.showinfo("Saved", f"Report saved:\n{saved}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))


def run_gui():
    root = tk.Tk()
    AnalyzerApp(root)
    root.mainloop()
