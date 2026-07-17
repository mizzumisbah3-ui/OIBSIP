import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_FILE = "bmi_records.db"


class BMIDatabase:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        weight REAL NOT NULL,
                        height REAL NOT NULL,
                        bmi REAL NOT NULL,
                        category TEXT NOT NULL,
                        recorded_at TEXT NOT NULL
                    )
                """)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not initialise database:\n{e}")
            raise SystemExit(1)

    def add_record(self, username, weight, height, bmi, category):
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO records (username, weight, height, bmi, category, recorded_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (username, weight, height, bmi, category, datetime.now().isoformat(timespec="seconds")),
                )
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not save record:\n{e}")
            return False

    def get_users(self):
        try:
            with self._connect() as conn:
                rows = conn.execute("SELECT DISTINCT username FROM records ORDER BY username").fetchall()
            return [r[0] for r in rows]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not read users:\n{e}")
            return []

    def get_history(self, username):
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT recorded_at, bmi FROM records WHERE username = ? ORDER BY recorded_at",
                    (username,),
                ).fetchall()
            return rows
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not read history:\n{e}")
            return []


def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db"
    elif bmi < 25:
        return "Normal", "#2ecc71"
    elif bmi < 30:
        return "Overweight", "#f39c12"
    else:
        return "Obese", "#e74c3c"


class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")

        self.db = BMIDatabase()
        self._build_widgets()

    def _build_widgets(self):
        style = ttk.Style(self)
        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))

        ttk.Label(self, text="BMI Calculator", style="Header.TLabel").pack(pady=(15, 10))

        form = ttk.Frame(self)
        form.pack(pady=5)

        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(form, text="Weight (kg):").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        self.weight_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.weight_var, width=20).grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(form, text="Height (m):").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        self.height_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.height_var, width=20).grid(row=2, column=1, padx=5, pady=6)

        ttk.Button(self, text="Calculate & Save", command=self.on_calculate).pack(pady=15)

        self.result_frame = tk.Frame(self, bg="#dcdde1", height=90, width=340)
        self.result_frame.pack(pady=5)
        self.result_frame.pack_propagate(False)

        self.result_label = tk.Label(
            self.result_frame, text="Enter your details above",
            font=("Segoe UI", 13, "bold"), bg="#dcdde1", fg="#2f3640"
        )
        self.result_label.pack(expand=True)

        history_frame = ttk.Frame(self)
        history_frame.pack(pady=15)

        ttk.Label(history_frame, text="View trend for:").grid(row=0, column=0, padx=5)
        self.user_select = ttk.Combobox(history_frame, state="readonly", width=17)
        self.user_select.grid(row=0, column=1, padx=5)
        self.refresh_user_list()

        ttk.Button(history_frame, text="Show Graph", command=self.on_show_graph).grid(row=0, column=2, padx=5)

        ttk.Button(self, text="Refresh User List", command=self.refresh_user_list).pack(pady=5)

    def refresh_user_list(self):
        users = self.db.get_users()
        self.user_select["values"] = users
        if users:
            self.user_select.current(0)

    def on_calculate(self):
        name = self.name_var.get().strip()
        weight_raw = self.weight_var.get().strip()
        height_raw = self.height_var.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Please enter a name.")
            return

        try:
            weight = float(weight_raw)
            height = float(height_raw)
        except ValueError:
            messagebox.showerror("Input Error", "Weight and height must be numeric values.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return

        bmi = calculate_bmi(weight, height)
        category, color = classify_bmi(bmi)

        self.result_frame.configure(bg=color)
        self.result_label.configure(
            bg=color,
            fg="white",
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

        saved = self.db.add_record(name, weight, height, bmi, category)
        if saved:
            self.refresh_user_list()

    def on_show_graph(self):
        username = self.user_select.get()
        if not username:
            messagebox.showinfo("No User", "No users with saved records yet.")
            return

        history = self.db.get_history(username)
        if not history:
            messagebox.showinfo("No Data", f"No history found for {username}.")
            return

        dates = [datetime.fromisoformat(row[0]) for row in history]
        bmis = [row[1] for row in history]

        graph_win = tk.Toplevel(self)
        graph_win.title(f"BMI Trend — {username}")
        graph_win.geometry("600x450")

        fig, ax = plt.subplots(figsize=(6, 4.2), dpi=100)
        ax.plot(dates, bmis, marker="o", color="#2980b9", linewidth=2)
        ax.axhspan(18.5, 25, color="#2ecc71", alpha=0.1, label="Normal range")
        ax.set_title(f"BMI Trend for {username}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.grid(True, linestyle="--", alpha=0.5)
        fig.autofmt_xdate()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
