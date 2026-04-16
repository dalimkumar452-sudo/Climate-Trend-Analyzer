import streamlit as st
import os
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
# Importing the Modular Data Engine
from data_engine import ClimateDataEngine 

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Climate Trend Intelligence",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# 2. DATA PROCESSING (Using Engine)
# ==========================================
# This ensures the script knows exactly where it is located
BASE_DIR = Path(__file__).resolve().parent.parent 
APP_DIR = Path(__file__).resolve().parent

df_raw = ClimateDataEngine.generate_climate_data()
df, anomalies_log, mean_val = ClimateDataEngine.process_analytics(df_raw)

# Clean date format for display
anomalies_log['Date'] = pd.to_datetime(anomalies_log['Date']).dt.date

# ==========================================
# 3. DASHBOARD UI & METRICS
# ==========================================
st.title("🌍 Climate Trend & Anomaly Intelligence")
st.markdown("---")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Avg Temperature", f"{mean_val:.2f} °C")
k2.metric("Warming Gradient", "+0.06 °C / Year")
k3.metric("Max Recorded", f"{df['Temperature'].max():.2f} °C")
k4.metric("Extreme Events", f"{len(anomalies_log)} Detects")

# ==========================================
# 4. MAIN VISUALIZATION
# ==========================================
st.subheader("Historical Temperature Analysis & Trend Decomposition")
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Temperature'], 
    name='Monthly Variance', 
    line=dict(color='#8ecae6', width=1.5), 
    opacity=0.6
))
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Warming_Trend'], 
    name='Long-term Trend', 
    line=dict(color='#d00000', width=3)
))
fig.add_trace(go.Scatter(
    x=anomalies_log['Date'], y=anomalies_log['Temperature'], 
    mode='markers', name='Climate Anomaly', 
    marker=dict(color='black', size=10, symbol='x')
))

fig.update_layout(
    template="plotly_white", 
    xaxis_title="Time Horizon", 
    yaxis_title="Surface Temp (°C)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 5. SCREENSHOT SHOWING SECTION (SS)
# ==========================================
st.markdown("---")
st.subheader("📷 Project Interface Preview")

# Search logic for the screenshot in multiple possible locations
ss_filename = "dashboard_ss.png"
possible_paths = [
    BASE_DIR / ss_filename,          # Project root
    APP_DIR / ss_filename,           # Inside 'app' folder
    BASE_DIR / "assets" / ss_filename # Inside an 'assets' folder
]

found_path = None
for p in possible_paths:
    if p.exists():
        found_path = p
        break

if found_path:
    st.image(str(found_path), caption="Live Dashboard Analysis Overview", use_container_width=True)
else:
    st.warning(f"⚠️ Screenshot '{ss_filename}' not found. Please place it in: {BASE_DIR}")

# ==========================================
# 6. DATA TABLES & EXPORT
# ==========================================
st.subheader("🚨 Extreme Event Registry")
st.dataframe(
    anomalies_log[['Date', 'Temperature']].sort_values(by='Date', ascending=False), 
    use_container_width=True, 
    hide_index=True
)

# Auto Export logic using Pathlib for safety
output_dir = BASE_DIR / "outputs"
output_dir.mkdir(exist_ok=True)
anomalies_log.to_csv(output_dir / "climate_anomalies.csv", index=False)

st.sidebar.success("✅ Connected to Data Engine")