import string
import secrets

import tkinter as tk
from tkinter import ttk, messagebox

import pyperclip


AMBIGUOUS_CHARACTERS = "0O1lI"

secure_random = secrets.SystemRandom()

password_history = []  # holds up to the last 5 generated passwords (in memory only)


def build_character_pools(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    """Return a dict of {type_name: character_string} for each selected type."""
    pools = {}

    if use_upper:
        pools["upper"] = string.ascii_uppercase
    if use_lower:
        pools["lower"] = string.ascii_lowercase
    if use_digits:
        pools["digits"] = string.digits
    if use_symbols:
        pools["symbols"] = string.punctuation

    if exclude_ambiguous:
        for key in pools:
            pools[key] = "".join(c for c in pools[key] if c not in AMBIGUOUS_CHARACTERS)

    return pools


def generate_secure_password(length, pools):
    """
    Generate a password of the given length using the given character pools.
    Guarantees at least one character from each pool, fills the rest randomly,
    then shuffles securely so the guaranteed characters aren't always at the start.
    """
    password_characters = []

    # Guarantee at least one character from each selected type
    for pool in pools.values():
        password_characters.append(secure_random.choice(pool))

    # Fill the remaining length from the combined pool
    combined_pool = "".join(pools.values())
    remaining = length - len(password_characters)
    for _ in range(remaining):
        password_characters.append(secure_random.choice(combined_pool))

    secure_random.shuffle(password_characters)
    return "".join(password_characters)


def calculate_strength(password, type_count):
    """Return (label, color, progress_percent) based on length and character diversity."""
    length = len(password)
    score = 0

    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    score += (type_count - 1)  # 0 to 3 extra points for diversity

    if score <= 1:
        return "Weak", "#EF4444", 33
    elif score <= 3:
        return "Medium", "#F59E0B", 66
    else:
        return "Strong", "#22C55E", 100


def on_generate_click():
    try:
        length = int(length_spinbox.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Length must be a whole number.")
        return

    if length < 8:
        messagebox.showerror("Invalid Input", "Password length must be at least 8 characters.")
        return

    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    exclude_ambiguous = ambiguous_var.get()

    type_count = sum([use_upper, use_lower, use_digits, use_symbols])
    if type_count < 2:
        messagebox.showerror("Invalid Input", "Please select at least 2 character types.")
        return

    pools = build_character_pools(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)

    empty_pools = [name for name, chars in pools.items() if len(chars) == 0]
    if empty_pools:
        messagebox.showerror(
            "Invalid Input",
            "Excluding ambiguous characters removed all characters from one of the "
            "selected types. Please deselect 'Exclude ambiguous characters' or choose "
            "different character types."
        )
        return

    password = generate_secure_password(length, pools)

    password_var.set(password)

    label, color, percent = calculate_strength(password, type_count)
    strength_label.config(text=f"Strength: {label}", fg=color)
    strength_bar["value"] = percent
    strength_bar_style.configure("Strength.Horizontal.TProgressbar", background=color)

    pyperclip.copy(password)
    copy_status_label.config(text="Copied to clipboard!")

    add_to_history(password)


def on_copy_click():
    password = password_var.get()
    if not password:
        messagebox.showwarning("Nothing to Copy", "Generate a password first.")
        return
    pyperclip.copy(password)
    copy_status_label.config(text="Copied to clipboard!")


def add_to_history(password):
    password_history.insert(0, password)
    if len(password_history) > 5:
        password_history.pop()

    history_listbox.delete(0, tk.END)
    for item in password_history:
        history_listbox.insert(tk.END, item)


root = tk.Tk()
root.title("Password Generator")
root.geometry("460x560")
root.resizable(False, False)
root.configure(bg="#F8FAFC")

tk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold"), bg="#F8FAFC").pack(pady=(15, 10))

length_frame = tk.Frame(root, bg="#F8FAFC")
length_frame.pack(pady=5)

tk.Label(length_frame, text="Password length:", bg="#F8FAFC").grid(row=0, column=0, padx=5)
length_spinbox = tk.Spinbox(length_frame, from_=8, to=64, width=5)
length_spinbox.delete(0, tk.END)
length_spinbox.insert(0, "12")
length_spinbox.grid(row=0, column=1, padx=5)

options_frame = tk.Frame(root, bg="#F8FAFC")
options_frame.pack(pady=10)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
ambiguous_var = tk.BooleanVar(value=False)

tk.Checkbutton(options_frame, text="Uppercase letters (A-Z)", variable=upper_var, bg="#F8FAFC").pack(anchor="w")
tk.Checkbutton(options_frame, text="Lowercase letters (a-z)", variable=lower_var, bg="#F8FAFC").pack(anchor="w")
tk.Checkbutton(options_frame, text="Numbers (0-9)", variable=digits_var, bg="#F8FAFC").pack(anchor="w")
tk.Checkbutton(options_frame, text="Symbols (!@#$...)", variable=symbols_var, bg="#F8FAFC").pack(anchor="w")
tk.Checkbutton(
    options_frame, text="Exclude ambiguous characters (0, O, 1, l, I)",
    variable=ambiguous_var, bg="#F8FAFC"
).pack(anchor="w")

tk.Button(
    root, text="Generate Password", command=on_generate_click,
    bg="#2563EB", fg="white", relief="flat", padx=10, pady=5
).pack(pady=15)

password_var = tk.StringVar()
password_entry = tk.Entry(
    root, textvariable=password_var, font=("Courier", 14), justify="center",
    state="readonly", readonlybackground="#E5E7EB"
)
password_entry.pack(fill="x", padx=20, pady=5)

copy_frame = tk.Frame(root, bg="#F8FAFC")
copy_frame.pack(pady=5)

tk.Button(
    copy_frame, text="Copy to Clipboard", command=on_copy_click,
    bg="#16A34A", fg="white", relief="flat", padx=10, pady=5
).pack(side="left", padx=5)

copy_status_label = tk.Label(copy_frame, text="", bg="#F8FAFC", fg="#16A34A")
copy_status_label.pack(side="left", padx=5)

strength_frame = tk.Frame(root, bg="#F8FAFC")
strength_frame.pack(pady=15, fill="x", padx=20)

strength_label = tk.Label(strength_frame, text="Strength: -", font=("Helvetica", 12, "bold"), bg="#F8FAFC")
strength_label.pack(anchor="w")

strength_bar_style = ttk.Style()
strength_bar_style.theme_use("default")
strength_bar_style.configure("Strength.Horizontal.TProgressbar", thickness=14)

strength_bar = ttk.Progressbar(
    strength_frame, style="Strength.Horizontal.TProgressbar",
    orient="horizontal", length=400, mode="determinate", maximum=100
)
strength_bar.pack(fill="x", pady=5)

history_frame = tk.Frame(root, bg="#F8FAFC")
history_frame.pack(pady=10, fill="both", expand=True, padx=20)

tk.Label(history_frame, text="Recent passwords (this session only):", bg="#F8FAFC").pack(anchor="w")

history_listbox = tk.Listbox(history_frame, height=5, font=("Courier", 10))
history_listbox.pack(fill="both", expand=True, pady=5)

root.mainloop()
