# green_building_dashboard.py

import streamlit as st
import random
import time

# --- AI Logic ---
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
        if occupancy:
            if temperature > self.temperature_threshold:
                hvac_status = f"Cooling ON ({temperature:.1f}°C)"
            elif temperature < self.temperature_threshold - 2:
                hvac_status = f"Heating ON ({temperature:.1f}°C)"
            else:
                hvac_status = "Standby"
            light_status = f"Lights ON ({light:.1f} Lux)" if light < self.light_threshold else "Lights OFF"
        else:
            hvac_status = "OFF (No occupancy)"
            light_status = "OFF (No occupancy)"
        return hvac_status, light_status

# --- Streamlit UI ---
st.set_page_config(page_title="Green Building AI", layout="centered")
st.title("🏢 Green Building Automation Dashboard")
st.markdown("AI-based control for HVAC and Lighting Systems")

ai = GreenBuildingAI()

# Sidebar controls
auto_mode = st.sidebar.checkbox("Auto Mode", value=True)
ai.auto_mode = auto_mode
refresh = st.sidebar.button("🔄 Manual Refresh")

# Session state to keep logs and data
if 'log' not in st.session_state:
    st.session_state.log = []

# Get sensor data and decisions
if auto_mode or refresh:
    temperature, light, occupancy = ai.get_sensor_data()
    hvac_status, light_status = ai.make_decision(temperature, light, occupancy)

    # Display status
    st.metric("🌡️ Temperature", f"{temperature:.1f} °C")
    st.metric("💡 Light Level", f"{light:.1f} Lux")
    st.metric("🚶‍♂️ Occupancy", "Yes" if occupancy else "No")
    st.success(f"HVAC Status: {hvac_status}")
    st.info(f"Lighting Status: {light_status}")

    # Log entry
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] Temp: {temperature:.1f}°C, Light: {light:.1f} Lux, " \
                f"Occupancy: {'Yes' if occupancy else 'No'}, HVAC: {hvac_status}, Lights: {light_status}"
    st.session_state.log.append(log_entry)

# Show logs
st.subheader("📜 System Logs")
for log in reversed(st.session_state.log[-10:]):  # show last 10 logs
    st.text(log)
