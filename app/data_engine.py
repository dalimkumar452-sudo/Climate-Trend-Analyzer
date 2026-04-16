import pandas as pd
import numpy as np

class ClimateDataEngine:
    @staticmethod
    def generate_climate_data():
        """Generates synthetic climate data."""
        dates = pd.date_range(start='2006-01-01', periods=240, freq='ME')
        base_temp = 21.5
        seasonal_effect = 11 * np.sin(2 * np.pi * np.arange(240) / 12)
        warming_slope = 0.06 * np.arange(240) / 12
        random_noise = np.random.normal(0, 1.3, 240)
        
        temperatures = base_temp + seasonal_effect + warming_slope + random_noise
        
        # Injecting anomalies
        anomaly_indices = [35, 72, 115, 160, 210, 230]
        for idx in anomaly_indices:
            temperatures[idx] += np.random.uniform(7.0, 10.0)
            
        return pd.DataFrame({'Date': dates, 'Temperature': temperatures})

    @staticmethod
    def process_analytics(df):
        """Statistical calculations."""
        df['Warming_Trend'] = df['Temperature'].rolling(window=12, center=True).mean()
        mean_val = df['Temperature'].mean()
        std_val = df['Temperature'].std()
        upper_limit = mean_val + (1.8 * std_val)
        
        df['Is_Anomaly'] = df['Temperature'] > upper_limit
        anomalies_log = df[df['Is_Anomaly']].copy()
        
        return df, anomalies_log, mean_val