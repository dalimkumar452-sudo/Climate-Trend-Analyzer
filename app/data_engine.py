-import pandas as pd
import numpy as np

class ClimateDataEngine:
    @staticmethod
    def generate_climate_data():
        """Generates synthetic climate data for analysis."""
        dates = pd.date_range(start="2010-01-01", end="2025-12-31", freq='M')
        
        # Creating a baseline temperature with a rising trend
        base_temp = 15 + (np.arange(len(dates)) * 0.05) 
        seasonal_effect = 10 * np.sin(np.arange(len(dates)) * (2 * np.pi / 12))
        noise = np.random.normal(0, 1.5, len(dates))
        
        temp = base_temp + seasonal_effect + noise
        
        # Adding artificial anomalies (extreme spikes)
        spike_indices = np.random.choice(len(temp), 8, replace=False)
        temp[spike_indices] += 8 
        
        return pd.DataFrame({'Date': dates, 'Temperature': temp})

    @staticmethod
    def process_analytics(df):
        """Calculates trends and detects anomalies."""
        # Calculate 12-month rolling average for the warming trend
        df['Warming_Trend'] = df['Temperature'].rolling(window=12, center=True).mean()
        
        # Anomaly Detection (Threshold: Mean + 2 Standard Deviations)
        mean = df['Temperature'].mean()
        std = df['Temperature'].std()
        anomalies = df[df['Temperature'] > (mean + 2 * std)].copy()
        
        return df, anomalies, mean