import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from pathlib import Path

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# SETTINGS
DB_FILE = Path(__file__).with_name("bmi_records.db")

# Colour to show for each BMI category
CATEGORY_COLORS = {
    "Underweight": "#3B82F6",    # blue
    "Normal weight": "#22C55E",  # green
    "Overweight": "#F59E0B",     # amber
    "Obese": "#EF4444",          # red
}

# This will hold the last calculated result so the Save button can use it
last_result = None  # will become (name, weight, height, bmi, category)


# DATABASE FUNCTIONS
def setup_database():
    """Create the records table if it doesn't already exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not set up database:\n{error}")


def save_record_to_db(name, weight, height, bmi, category):
    """Insert one BMI record into the database. Returns True if it worked."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute(
            "INSERT INTO records (name, weight, height, bmi, category, recorded_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, weight, height, bmi, category, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not save record:\n{error}")
        return False


def get_all_user_names():
    """Return a list of all distinct user names saved in the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        rows = conn.execute("SELECT DISTINCT name FROM records ORDER BY name").fetchall()
        conn.close()
        return [row[0] for row in rows]
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not load users:\n{error}")
        return []


def get_history_for_user(name):
    """Return a list of (date, bmi) tuples for the given user, oldest first."""
    try:
        conn = sqlite3.connect(DB_FILE)
        rows = conn.execute(
            "SELECT recorded_at, bmi FROM records WHERE name = ? ORDER BY recorded_at",
            (name,)
        ).fetchall()
        conn.close()
        return rows
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not load history:\n{error}")
        return []


# BMI CALCULATION FUNCTIONS
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# BUTTON ACTIONS
def on_calculate_click():
    """Runs when the user presses the 'Calculate' button."""
    global last_result

    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # --- validation ---
    if name == "":
        messagebox.showerror("Invalid Input", "Please enter a name.")
        return

    try:
        weight = float(weight_text)
    except ValueError:
        messagebox.showerror("Invalid Input", "Weight must be a number, e.g. 70")
        return

    try:
        height = float(height_text)
    except ValueError:
        messagebox.showerror("Invalid Input", "Height must be a number, e.g. 1.75")
        return

    if weight <= 0 or height <= 0:
        messagebox.showerror("Invalid Input", "Weight and height must be positive numbers.")
        return

    # --- calculation ---
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    color = CATEGORY_COLORS[category]

    # --- show result ---
    result_label.config(
        text=f"{name}: BMI = {bmi:.2f}  ->  {category}",
        bg=color,
        fg="white"
    )

    last_result = (name, weight, height, bmi, category)


def on_save_click():
    """Runs when the user presses the 'Save Record' button."""
    if last_result is None:
        messagebox.showwarning("Nothing to Save", "Press Calculate first.")
        return

    name, weight, height, bmi, category = last_result
    success = save_record_to_db(name, weight, height, bmi, category)

    if success:
        messagebox.showinfo("Saved", f"Record saved for {name}.")
        refresh_user_dropdown(select_name=name)


def refresh_user_dropdown(select_name=None):
    """Reload the list of users into the dropdown box."""
    names = get_all_user_names()
    user_dropdown["values"] = names

    if select_name and select_name in names:
        user_dropdown.set(select_name)
    elif names:
        user_dropdown.set(names[0])


def on_show_graph_click():
    """Runs when the user presses 'Show Trend Graph'. Opens a new window with the chart."""
    name = user_dropdown.get()

    if not name:
        messagebox.showwarning("No User Selected", "Save at least one record first, then pick a user.")
        return

    history = get_history_for_user(name)

    if len(history) == 0:
        messagebox.showinfo("No Data", f"No saved records for {name} yet.")
        return

    dates = [datetime.fromisoformat(row[0]) for row in history]
    bmi_values = [row[1] for row in history]

    # Open a brand new window just for the graph
    graph_window = tk.Toplevel(root)
    graph_window.title(f"BMI Trend - {name}")
    graph_window.geometry("560x420")

    figure = Figure(figsize=(5.4, 3.8), dpi=100)
    plot = figure.add_subplot(111)
    plot.plot(dates, bmi_values, marker="o", color="#2563EB", linewidth=2)
    plot.axhline(18.5, color="#94A3B8", linestyle="--", linewidth=0.8)
    plot.axhline(25, color="#94A3B8", linestyle="--", linewidth=0.8)
    plot.axhline(30, color="#94A3B8", linestyle="--", linewidth=0.8)
    plot.set_title(f"BMI Trend - {name}")
    plot.set_ylabel("BMI")

    # If there's only one record, matplotlib's auto date-range can span years,
    # which looks misleading. Give it a small, sensible window instead.
    if len(dates) == 1:
        plot.set_xlim(dates[0] - timedelta(days=7), dates[0] + timedelta(days=7))

    figure.autofmt_xdate(rotation=30)
    figure.tight_layout()

    canvas = FigureCanvasTkAgg(figure, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# BUILD THE WINDOW
setup_database()

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("480x400")
root.resizable(False, False)
root.configure(bg="#F8FAFC")

# --- Title ---
tk.Label(root, text="BMI Calculator", font=("Helvetica", 18, "bold"), bg="#F8FAFC").pack(pady=(15, 10))

# --- Input form ---
form_frame = tk.Frame(root, bg="#F8FAFC")
form_frame.pack(pady=5)

tk.Label(form_frame, text="Name:", bg="#F8FAFC").grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Weight (kg):", bg="#F8FAFC").grid(row=1, column=0, sticky="w", pady=5)
weight_entry = tk.Entry(form_frame, width=25)
weight_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Height (m):", bg="#F8FAFC").grid(row=2, column=0, sticky="w", pady=5)
height_entry = tk.Entry(form_frame, width=25)
height_entry.grid(row=2, column=1, pady=5)

# --- Calculate button ---
tk.Button(
    root, text="Calculate", command=on_calculate_click,
    bg="#2563EB", fg="white", relief="flat", padx=10, pady=5
).pack(pady=10)

# --- Result label ---
result_label = tk.Label(
    root, text="Enter your details and press Calculate",
    font=("Helvetica", 12), bg="#E5E7EB", fg="#111827",
    padx=10, pady=12, wraplength=420, justify="center"
)
result_label.pack(fill="x", padx=20)

# --- Save + graph controls ---
action_frame = tk.Frame(root, bg="#F8FAFC")
action_frame.pack(pady=15)

tk.Button(
    action_frame, text="Save Record", command=on_save_click,
    bg="#16A34A", fg="white", relief="flat", padx=10, pady=5
).grid(row=0, column=0, padx=5)

tk.Label(action_frame, text="View history for:", bg="#F8FAFC").grid(row=0, column=1, padx=5)

user_dropdown = ttk.Combobox(action_frame, state="readonly", width=12)
user_dropdown.grid(row=0, column=2, padx=5)

tk.Button(
    action_frame, text="Show Trend Graph", command=on_show_graph_click,
    bg="#7C3AED", fg="white", relief="flat", padx=10, pady=5
).grid(row=0, column=3, padx=5)

# Load any existing users into the dropdown when the app starts
refresh_user_dropdown()

# --- Start the app ---
root.mainloop()
