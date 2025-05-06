import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class GreenBuildingAI:
    def __init__(self):
        self.temperature_threshold = 24  # Celsius
        self.light_threshold = 300       # Lux
        self.auto_mode = True

    def get_sensor_data(self):
        temperature = random.uniform(18, 32)
        light = random.uniform(100, 700)
        occupancy = random.choice([True, False])
        return temperature, light, occupancy

    def make_decision(self, temperature, light, occupancy):
        hvac_status = "OFF"
        light_status = "OFF"

        if occupancy:
            if temperature > self.temperature_threshold:
                hvac_status = f"Cooling ON ({temperature:.1f}°C)"
            elif temperature < self.temperature_threshold - 2:
                hvac_status = f"Heating ON ({temperature:.1f}°C)"
            else:
                hvac_status = "Standby"

            if light < self.light_threshold:
                light_status = f"Lights ON ({light:.1f} Lux)"
            else:
                light_status = "Lights OFF"
        else:
            hvac_status = "OFF (No occupancy)"
            light_status = "OFF (No occupancy)"

        return hvac_status, light_status

class GreenBuildingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Green Building Automation Dashboard")
        self.ai = GreenBuildingAI()

        # UI Setup
        self.setup_ui()
        self.running = True
        self.auto_update()

    def setup_ui(self):
        self.temp_label = ttk.Label(self.root, text="Temperature: ", font=("Arial", 12))
        self.temp_label.pack(pady=5)

        self.light_label = ttk.Label(self.root, text="Light: ", font=("Arial", 12))
        self.light_label.pack(pady=5)

        self.occupancy_label = ttk.Label(self.root, text="Occupancy: ", font=("Arial", 12))
        self.occupancy_label.pack(pady=5)

        self.hvac_label = ttk.Label(self.root, text="HVAC Status: ", font=("Arial", 12, "bold"))
        self.hvac_label.pack(pady=5)

        self.lighting_label = ttk.Label(self.root, text="Lighting Status: ", font=("Arial", 12, "bold"))
        self.lighting_label.pack(pady=5)

        self.log_box = tk.Text(self.root, height=10, width=60, state='disabled', bg="#f0f0f0")
        self.log_box.pack(pady=10)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack()

        self.refresh_button = ttk.Button(self.button_frame, text="Manual Refresh", command=self.update_status)
        self.refresh_button.grid(row=0, column=0, padx=10)

        self.auto_toggle = ttk.Checkbutton(self.button_frame, text="Auto Mode", command=self.toggle_auto)
        self.auto_toggle.state(['!alternate', 'selected'])
        self.auto_toggle.grid(row=0, column=1)

    def toggle_auto(self):
        self.ai.auto_mode = not self.ai.auto_mode

    def update_status(self):
        temp, light, occ = self.ai.get_sensor_data()
        hvac_status, light_status = self.ai.make_decision(temp, light, occ)

        self.temp_label.config(text=f"Temperature: {temp:.1f} °C")
        self.light_label.config(text=f"Light: {light:.1f} Lux")
        self.occupancy_label.config(text=f"Occupancy: {'Yes' if occ else 'No'}")
        self.hvac_label.config(text=f"HVAC Status: {hvac_status}")
        self.lighting_label.config(text=f"Lighting Status: {light_status}")

        log_msg = f"[{time.strftime('%H:%M:%S')}] Temp: {temp:.1f}°C, Light: {light:.1f} Lux, " \
                  f"Occ: {occ}, HVAC: {hvac_status}, Lights: {light_status}\n"
        self.log(log_msg)

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message)
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

    def auto_update(self):
        if self.ai.auto_mode and self.running:
            self.update_status()
        self.root.after(3000, self.auto_update)  # refresh every 3 seconds

    def stop(self):
        self.running = False

if
