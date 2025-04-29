import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.stats import chi2

class ChiSquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chi-Square Calculator")

        # Input for number of rows and columns
        tk.Label(root, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(root, text="Columns:").grid(row=0, column=2, padx=5, pady=5)

        self.row_entry = tk.Entry(root, width=5)
        self.col_entry = tk.Entry(root, width=5)
        self.row_entry.grid(row=0, column=1)
        self.col_entry.grid(row=0, column=3)

        self.set_grid_button = tk.Button(root, text="Set Grid", command=self.create_grid)
        self.set_grid_button.grid(row=0, column=4, padx=5)

        self.entries = []
        self.result_label = None

    def create_grid(self):
        # Clear previous entries and result
        for row in self.entries:
            for entry in row:
                entry.destroy()
        self.entries.clear()
        if self.result_label:
            self.result_label.config(text="")

        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())
            if self.rows < 2 or self.cols < 2:
                raise ValueError("Minimum size is 2x2")

            # Create entry grid
            for i in range(self.rows):
                row_entries = []
                for j in range(self.cols):
                    entry = tk.Entry(self.root, width=5)
                    entry.grid(row=i+1, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Buttons
            calc_button = tk.Button(self.root, text="Calculate", command=self.calculate)
            calc_button.grid(row=self.rows+2, column=0, columnspan=2, pady=10)

            clear_button = tk.Button(self.root, text="Clear", command=self.clear)
            clear_button.grid(row=self.rows+2, column=2, columnspan=2)

            # Result Label
            self.result_label = tk.Label(self.root, text="", justify="left", font=("Courier", 10), anchor="w")
            self.result_label.grid(row=self.rows+3, column=0, columnspan=self.cols+2, padx=10, pady=10)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers ≥ 2 for rows and columns.")

    def calculate(self):
        try:
            obs = np.array([[int(entry.get()) for entry in row] for row in self.entries])

            row_totals = obs.sum(axis=1)
            col_totals = obs.sum(axis=0)
            grand_total = obs.sum()

            expected = np.outer(row_totals, col_totals) / grand_total
            chi_sq = ((obs - expected) ** 2 / expected).sum()
            df = (obs.shape[0] - 1) * (obs.shape[1] - 1)
            p_value = chi2.sf(chi_sq, df)

            result_text = (
                f"Observed:\n{obs}\n\n"
                f"Expected:\n{expected.round(2)}\n\n"
                f"Chi-Square Statistic: {chi_sq:.4f}\n"
                f"Degrees of Freedom: {df}\n"
                f"P-Value: {p_value:.4f}"
            )
            self.result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Invalid input", "Please fill all cells with whole numbers.")

    def clear(self):
        # Clear row/column entry fields
        self.row_entry.delete(0, tk.END)
        self.col_entry.delete(0, tk.END)

        # Destroy grid entry widgets
        for row in self.entries:
            for entry in row:
                entry.destroy()
        self.entries.clear()

        # Remove result label
        if self.result_label:
            self.result_label.destroy()
            self.result_label = None

        # Destroy buttons if present
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) >= self.rows + 2:
                widget.destroy()


# Run the app
root = tk.Tk()
app = ChiSquareApp(root)
root.mainloop()
