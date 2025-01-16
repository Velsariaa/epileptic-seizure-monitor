import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self, detector, logic):
        self.detector = detector
        self.logic = logic
        self.root = tk.Tk()
        self.root.geometry("850x450")
        self.root.title("Epileptic Seizure Monitor")

        # Load Azure theme
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")  # Default to dark mode

        self.is_dark_mode = True

        self.setup_frontpage()

    def create_toggle_bar(self):
        """Toggle bar with a switch button for theme switching."""
        toggle_frame = ttk.Frame(self.root)
        toggle_frame.place(relx=0.85, rely=0.02, relwidth=0.17, relheight=0.08)

        # Variable to track switch state
        self.theme_var = tk.BooleanVar(value=self.is_dark_mode)

        # Switch-style Checkbutton
        self.switch_button = ttk.Checkbutton(
            toggle_frame,
            text="Dark Mode",
            style="Switch.TCheckbutton",
            variable=self.theme_var,
            command=self.switch_theme,
        )
        self.switch_button.pack(fill="both", expand=True)

    def switch_theme(self):
        """Switch the theme using Azure theme's built-in function."""
        self.is_dark_mode = self.theme_var.get()
        theme = "dark" if self.is_dark_mode else "light"
        self.root.tk.call("set_theme", theme)
        self.switch_button.config(text="Dark Mode" if self.is_dark_mode else "Light Mode")

    def setup_frontpage(self):
        title = "Welcome to EpilepSafe"
        description = (
            "Empowering individuals with epilepsy with a tool designed to enhance safety, "
            "promote awareness, and foster a better quality of life. Experience peace of "
            "mind through innovative features tailored to meet your unique needs."
        )

        # Create the toggle bar for theme
        self.create_toggle_bar()

        title_label = ttk.Label(
            self.root,
            text=title,
            wraplength=400,
            justify="left",
            font=("Arial", 24, "bold"),
        )
        title_label.place(relx=0.04, rely=0.20, relwidth=0.5, relheight=0.1)

        description_label = ttk.Label(
            self.root,
            text=description,
            wraplength=400,
            justify="left",
            font=("Arial", 16),
        )
        description_label.place(relx=0.04, rely=0.30, relwidth=0.55, relheight=0.5)

        self.setup_settings()

    def setup_settings(self):
        settings_frame = ttk.Frame(self.root)
        settings_frame.place(relx=0.54, rely=0.15, relwidth=0.20, relheight=1)

        def save_settings():
            try:
                self.detector.dangerous_freq_min = float(dangerous_freq_min_spinbox.get())
                self.detector.dangerous_freq_max = float(dangerous_freq_max_spinbox.get())
                self.detector.intensity_change_thresh = float(intensity_change_thresh_spinbox.get())
                self.detector.consecutive_threshold = int(consecutive_threshold_spinbox.get())
                self.detector.alert_cooldown = int(alert_cooldown_spinbox.get())
                self.detector.window_trigger_behavior = window_behavior_var.get()
                messagebox.showinfo("Settings Saved", "Settings have been successfully updated.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for all settings.")

        ttk.Label(settings_frame, text="Dangerous Frequency Min:").pack()
        dangerous_freq_min_spinbox = ttk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_min_spinbox.delete(0, "end")
        dangerous_freq_min_spinbox.insert(0, str(self.detector.dangerous_freq_min))
        dangerous_freq_min_spinbox.pack()

        ttk.Label(settings_frame, text="Dangerous Frequency Max:").pack()
        dangerous_freq_max_spinbox = ttk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_max_spinbox.delete(0, "end")
        dangerous_freq_max_spinbox.insert(0, str(self.detector.dangerous_freq_max))
        dangerous_freq_max_spinbox.pack()

        ttk.Label(settings_frame, text="Intensity Change Threshold:").pack()
        intensity_change_thresh_spinbox = ttk.Spinbox(settings_frame, from_=0, to=1, increment=0.01)
        intensity_change_thresh_spinbox.delete(0, "end")
        intensity_change_thresh_spinbox.insert(0, str(self.detector.intensity_change_thresh))
        intensity_change_thresh_spinbox.pack()

        ttk.Label(settings_frame, text="Consecutive Threshold:").pack()
        consecutive_threshold_spinbox = ttk.Spinbox(settings_frame, from_=1, to=10, increment=1)
        consecutive_threshold_spinbox.delete(0, "end")
        consecutive_threshold_spinbox.insert(0, str(self.detector.consecutive_threshold))
        consecutive_threshold_spinbox.pack()

        ttk.Label(settings_frame, text="Alert Cooldown:").pack()
        alert_cooldown_spinbox = ttk.Spinbox(settings_frame, from_=1, to=60, increment=1)
        alert_cooldown_spinbox.delete(0, "end")
        alert_cooldown_spinbox.insert(0, str(self.detector.alert_cooldown))
        alert_cooldown_spinbox.pack()

        ttk.Label(settings_frame, text="Window Behavior:").pack()
        window_behavior_var = tk.StringVar(value=self.detector.window_trigger_behavior)
        window_behavior_dropdown = ttk.OptionMenu(settings_frame, window_behavior_var, "minimize", "close", "minimize")
        window_behavior_dropdown.pack()

        save_button = ttk.Button(settings_frame, text="Save", command=save_settings)
        save_button.pack(pady=10)

    def show_alert(self):
        message = ""

        if self.detector.window_trigger_behavior == "minimize":
            message = "Content minimized."

        elif self.detector.window_trigger_behavior == "close":
            message = "Content closed."

        self.root.after(0, lambda: messagebox.showwarning(
            "Warning", f"Potential seizure-inducing content detected! \n{message}"
        ))

    def run(self):
        self.root.mainloop()
