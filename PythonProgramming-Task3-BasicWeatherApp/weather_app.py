import os
import io
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import requests

try:
    from PIL import Image, ImageTk
except ImportError:
    raise SystemExit(
        "Pillow is required for weather icons. Install it with:\n"
        "    pip install pillow"
    )

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "5312fb8bd268b796b21986c9a243ab1a")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL_TEMPLATE = "https://openweathermap.org/img/wn/{icon}@2x.png"
IPINFO_URL = "https://ipinfo.io/json"

REQUEST_TIMEOUT_SECONDS = 8

class WeatherAPIError(Exception):
    """Raised for any recoverable weather-API problem (shown to the user)."""


class WeatherAPI:
    """Thin wrapper around the OpenWeatherMap endpoints used by this app."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, url: str, params: dict) -> dict:
        params = {**params, "appid": self.api_key}
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        except requests.exceptions.Timeout:
            raise WeatherAPIError("The request timed out. Check your internet connection and try again.")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Could not connect. Check your internet connection.")
        except requests.exceptions.RequestException as exc:
            raise WeatherAPIError(f"Network error: {exc}")

        if response.status_code == 401:
            raise WeatherAPIError(
                "Invalid API key. Set OPENWEATHER_API_KEY or edit API_KEY in weather_app.py.\n"
                "Note: new OpenWeatherMap keys can take up to 2 hours to activate."
            )
        if response.status_code == 404:
            raise WeatherAPIError("Location not found. Check the spelling and try again.")
        if response.status_code == 429:
            raise WeatherAPIError("Too many requests. Please wait a moment and try again.")
        if not response.ok:
            raise WeatherAPIError(f"Weather service error (HTTP {response.status_code}).")

        try:
            return response.json()
        except ValueError:
            raise WeatherAPIError("Received an invalid response from the weather service.")

    def get_current_weather(self, city: str) -> dict:
        return self._get(CURRENT_WEATHER_URL, {"q": city, "units": "metric"})

    def get_forecast(self, city: str) -> dict:
        return self._get(FORECAST_URL, {"q": city, "units": "metric"})

    @staticmethod
    def get_icon_image(icon_code: str, size=(60, 60)):
        """Download a weather icon and return a Tk-compatible PhotoImage."""
        url = ICON_URL_TEMPLATE.format(icon=icon_code)
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content)).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception:
            return None  # Icon is a nice-to-have; never crash the app over it.

    @staticmethod
    def detect_city_by_ip() -> str:
        """Bonus feature: guess the user's city from their public IP address."""
        try:
            response = requests.get(IPINFO_URL, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            city = data.get("city")
            if not city:
                raise WeatherAPIError("Could not determine your city from your IP address.")
            return city
        except requests.exceptions.RequestException:
            raise WeatherAPIError("Could not reach the location service.")

def extract_next_hours(forecast_json: dict, hours: int = 6) -> list:
    """
    Return forecast entries that fall within the next `hours` hours.
    The free API only provides 3-hour steps, so for hours=6 this
    typically returns 2 entries — each labeled with its real timestamp.
    """
    entries = []
    now = datetime.now()
    for item in forecast_json.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        if (dt - now).total_seconds() <= hours * 3600:
            entries.append(item)
        else:
            break
    return entries if entries else forecast_json.get("list", [])[:2]


def extract_daily_summary(forecast_json: dict, days: int = 5) -> list:
    """
    Collapse the 3-hour-step list into one representative entry per day
    (the reading closest to 12:00 local time), for the next `days` days.
    """
    by_date = {}
    for item in forecast_json.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        date_key = dt.date()
        hour_distance = abs(dt.hour - 12)
        if date_key not in by_date or hour_distance < by_date[date_key][0]:
            by_date[date_key] = (hour_distance, item)

    today = datetime.now().date()
    daily_items = [
        (date_key, item) for date_key, (_, item) in sorted(by_date.items())
        if date_key != today
    ]
    return daily_items[:days]


def c_to_f(celsius: float) -> float:
    return celsius * 9 / 5 + 32

class WeatherApp(tk.Tk):
    BG = "#eaf2fb"
    CARD_BG = "#ffffff"
    ACCENT = "#2f6fed"
    TEXT = "#1c2b3a"
    MUTED = "#6b7c93"

    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("760x640")
        self.minsize(680, 600)
        self.configure(bg=self.BG)

        self.api = WeatherAPI(API_KEY)
        self.unit = "C"  # "C" or "F"
        self._icon_refs = []  # keep references so Tk doesn't garbage-collect images
        self._last_current = None  # cache last successful data for unit toggling
        self._last_forecast = None

        self._build_layout()

    def _build_layout(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=("Segoe UI", 10))
        style.configure("Accent.TButton", background=self.ACCENT, foreground="white")
        style.map("Accent.TButton", background=[("active", "#255ad1")])

        # --- Search bar ---
        search_frame = tk.Frame(self, bg=self.BG, pady=14)
        search_frame.pack(fill="x", padx=16)

        tk.Label(search_frame, text="City or ZIP code:", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 10)).pack(side="left")

        self.city_var = tk.StringVar()
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var, width=28,
                                     font=("Segoe UI", 11))
        self.city_entry.pack(side="left", padx=8)
        self.city_entry.bind("<Return>", lambda e: self.on_get_weather())

        ttk.Button(search_frame, text="Get Weather", style="Accent.TButton",
                   command=self.on_get_weather).pack(side="left", padx=4)
        ttk.Button(search_frame, text="📍 Use My Location",
                   command=self.on_detect_location).pack(side="left", padx=4)

        self.unit_button = ttk.Button(search_frame, text="Switch to °F",
                                       command=self.on_toggle_unit)
        self.unit_button.pack(side="right")

        # --- Error banner (hidden until needed) ---
        self.error_var = tk.StringVar()
        self.error_label = tk.Label(self, textvariable=self.error_var, bg="#fdecea",
                                     fg="#a4262c", font=("Segoe UI", 10, "bold"),
                                     wraplength=720, justify="left", anchor="w", padx=10, pady=8)
        # packed/unpacked dynamically by _show_error / _clear_error

        # --- Current conditions card ---
        self.current_card = tk.Frame(self, bg=self.CARD_BG, padx=20, pady=16)
        self.current_card.pack(fill="x", padx=16, pady=(4, 10))

        top_row = tk.Frame(self.current_card, bg=self.CARD_BG)
        top_row.pack(fill="x")

        self.icon_label = tk.Label(top_row, bg=self.CARD_BG)
        self.icon_label.pack(side="left")

        info_col = tk.Frame(top_row, bg=self.CARD_BG)
        info_col.pack(side="left", padx=16)

        self.city_title_var = tk.StringVar(value="Search for a city to begin")
        tk.Label(info_col, textvariable=self.city_title_var, bg=self.CARD_BG, fg=self.TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.temp_var = tk.StringVar(value="--°")
        tk.Label(info_col, textvariable=self.temp_var, bg=self.CARD_BG, fg=self.ACCENT,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w")

        self.desc_var = tk.StringVar(value="")
        tk.Label(info_col, textvariable=self.desc_var, bg=self.CARD_BG, fg=self.MUTED,
                 font=("Segoe UI", 11)).pack(anchor="w")

        details_row = tk.Frame(self.current_card, bg=self.CARD_BG, pady=10)
        details_row.pack(fill="x")

        self.humidity_var = tk.StringVar(value="Humidity: --%")
        self.wind_var = tk.StringVar(value="Wind: -- m/s")
        self.feels_var = tk.StringVar(value="Feels like: --°")

        for var in (self.humidity_var, self.wind_var, self.feels_var):
            tk.Label(details_row, textvariable=var, bg=self.CARD_BG, fg=self.TEXT,
                     font=("Segoe UI", 10)).pack(side="left", padx=(0, 24))

        # --- Hourly forecast panel ---
        tk.Label(self, text="Next hours", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=18)
        self.hourly_frame = tk.Frame(self, bg=self.BG)
        self.hourly_frame.pack(fill="x", padx=16, pady=(4, 10))

        # --- Daily forecast panel ---
        tk.Label(self, text="Next 5 days", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=18)
        self.daily_frame = tk.Frame(self, bg=self.BG)
        self.daily_frame.pack(fill="x", padx=16, pady=(4, 16))

        # --- Status bar ---
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self, textvariable=self.status_var, bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 9)).pack(side="bottom", anchor="w", padx=16, pady=6)

    def _show_error(self, message: str):
        self.error_var.set("⚠ " + message)
        self.error_label.pack(fill="x", padx=16, pady=(0, 8), before=self.current_card)

    def _clear_error(self):
        self.error_var.set("")
        self.error_label.pack_forget()


    def on_detect_location(self):
        self.status_var.set("Detecting your location…")

        def worker():
            try:
                city = self.api.detect_city_by_ip()
                self.after(0, lambda: self.city_var.set(city))
                self.after(0, self.on_get_weather)
            except WeatherAPIError as exc:
                self.after(0, lambda: self._show_error(str(exc)))
                self.after(0, lambda: self.status_var.set("Ready."))

        threading.Thread(target=worker, daemon=True).start()

    def on_get_weather(self):
        city = self.city_var.get().strip()

        # Input validation: reject empty input.
        if not city:
            self._show_error("Please enter a city name or ZIP code.")
            return

        self._clear_error()
        self.status_var.set(f"Fetching weather for '{city}'…")
        self.city_entry.config(state="disabled")

        def worker():
            try:
                current = self.api.get_current_weather(city)
                forecast = self.api.get_forecast(city)
            except WeatherAPIError as exc:
                self.after(0, lambda: self._on_fetch_failed(str(exc)))
                return
            self.after(0, lambda: self._on_fetch_success(current, forecast))

        threading.Thread(target=worker, daemon=True).start()

    def _on_fetch_failed(self, message: str):
        self.city_entry.config(state="normal")
        self.status_var.set("Ready.")
        self._show_error(message)

    def _on_fetch_success(self, current: dict, forecast: dict):
        self.city_entry.config(state="normal")
        self.status_var.set("Updated just now.")
        self._last_current = current
        self._last_forecast = forecast
        self._render_current(current)
        self._render_hourly(forecast)
        self._render_daily(forecast)

    def on_toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"
        self.unit_button.config(text=f"Switch to °{'C' if self.unit == 'F' else 'F'}")
        if self._last_current and self._last_forecast:
            self._render_current(self._last_current)
            self._render_hourly(self._last_forecast)
            self._render_daily(self._last_forecast)

    def _fmt_temp(self, celsius: float) -> str:
        if self.unit == "F":
            return f"{c_to_f(celsius):.0f}°F"
        return f"{celsius:.0f}°C"

    def _render_current(self, data: dict):
        name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        self.city_title_var.set(f"{name}, {country}" if country else name)

        main = data.get("main", {})
        weather = (data.get("weather") or [{}])[0]
        wind = data.get("wind", {})

        temp_c = main.get("temp", 0)
        feels_c = main.get("feels_like", 0)

        # Show both units at once for the beginner-tier requirement,
        # while the toggle controls which one is emphasized as primary.
        primary = self._fmt_temp(temp_c)
        secondary = f"{c_to_f(temp_c):.0f}°F" if self.unit == "C" else f"{temp_c:.0f}°C"
        self.temp_var.set(f"{primary}  ({secondary})")

        self.desc_var.set(weather.get("description", "").title())
        self.humidity_var.set(f"Humidity: {main.get('humidity', '--')}%")
        self.wind_var.set(f"Wind: {wind.get('speed', '--')} m/s")
        self.feels_var.set(f"Feels like: {self._fmt_temp(feels_c)}")

        icon_code = weather.get("icon")
        if icon_code:
            img = self.api.get_icon_image(icon_code, size=(72, 72))
            if img:
                self._icon_refs.append(img)
                self.icon_label.config(image=img)

    def _render_hourly(self, forecast: dict):
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        entries = extract_next_hours(forecast, hours=6)
        if not entries:
            tk.Label(self.hourly_frame, text="No hourly data available.",
                     bg=self.BG, fg=self.MUTED).pack(side="left")
            return

        for item in entries:
            dt = datetime.fromtimestamp(item["dt"])
            temp_c = item.get("main", {}).get("temp", 0)
            weather = (item.get("weather") or [{}])[0]

            cell = tk.Frame(self.hourly_frame, bg=self.CARD_BG, padx=12, pady=10)
            cell.pack(side="left", padx=6)

            tk.Label(cell, text=dt.strftime("%I %p").lstrip("0"), bg=self.CARD_BG,
                     fg=self.TEXT, font=("Segoe UI", 10, "bold")).pack()

            icon_code = weather.get("icon")
            if icon_code:
                img = self.api.get_icon_image(icon_code, size=(40, 40))
                if img:
                    self._icon_refs.append(img)
                    tk.Label(cell, image=img, bg=self.CARD_BG).pack()

            tk.Label(cell, text=self._fmt_temp(temp_c), bg=self.CARD_BG, fg=self.MUTED,
                     font=("Segoe UI", 10)).pack()

    def _render_daily(self, forecast: dict):
        for widget in self.daily_frame.winfo_children():
            widget.destroy()

        daily_items = extract_daily_summary(forecast, days=5)
        if not daily_items:
            tk.Label(self.daily_frame, text="No daily data available.",
                     bg=self.BG, fg=self.MUTED).pack(side="left")
            return

        for date_key, item in daily_items:
            temp_c = item.get("main", {}).get("temp", 0)
            weather = (item.get("weather") or [{}])[0]

            cell = tk.Frame(self.daily_frame, bg=self.CARD_BG, padx=12, pady=10)
            cell.pack(side="left", padx=6, expand=True, fill="x")

            tk.Label(cell, text=date_key.strftime("%a %d %b"), bg=self.CARD_BG,
                     fg=self.TEXT, font=("Segoe UI", 10, "bold")).pack()

            icon_code = weather.get("icon")
            if icon_code:
                img = self.api.get_icon_image(icon_code, size=(40, 40))
                if img:
                    self._icon_refs.append(img)
                    tk.Label(cell, image=img, bg=self.CARD_BG).pack()

            tk.Label(cell, text=self._fmt_temp(temp_c), bg=self.CARD_BG, fg=self.MUTED,
                     font=("Segoe UI", 10)).pack()
            tk.Label(cell, text=weather.get("main", ""), bg=self.CARD_BG, fg=self.MUTED,
                     font=("Segoe UI", 9)).pack()


def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        # We still launch the GUI so the user sees the proper in-app error
        # message (per the "errors shown in GUI, not terminal" requirement)
        # rather than crashing before the window even appears.
        print("Warning: no OPENWEATHER_API_KEY set. The app will show an "
              "'invalid API key' error until you configure one.")
    app = WeatherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
