import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

class SensorDataProcessor:
    def __init__(self, expected_ranges):
        """Initialize with expected ranges for sensor readings."""
        self.expected_ranges = expected_ranges
    
    def validate_and_clean(self, data):
        """Validates and cleans sensor data."""
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])  # Remove rows with invalid timestamps
        df = df.sort_values(by="timestamp")  # Handle out-of-sequence data
        df = df.drop_duplicates(subset=["timestamp"], keep='first')  # Remove duplicate readings
        
        # Handle out-of-range values
        for col, (min_val, max_val) in self.expected_ranges.items():
            df[col] = df[col].apply(lambda x: np.nan if x < min_val or x > max_val else x)
        
        # Fill missing values using interpolation
        df = df.interpolate(method='linear')
        return df

# Define expected ranges for sensor data
expected_ranges = {
    "temperature": (-40, 85),  # Celsius
    "humidity": (0, 100),  # Percentage
    "pressure": (900, 1100),  # hPa
    "battery": (0, 100)  # Percentage
}

sensor_data = [
    {"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": 25.5, "humidity": 60, "pressure": 1013.25, "battery": 85},
    {"device_id": "sensor_123", "timestamp": "2025-01-29T14:31:00Z", "temperature": -50, "humidity": 110, "pressure": 1200, "battery": 105},
    {"device_id": "sensor_123", "timestamp": "2025-01-29T14:32:00Z", "temperature": 26, "humidity": 61, "pressure": 1014, "battery": 84},
    {"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": 25.5, "humidity": 60, "pressure": 1013.25, "battery": 85},  # Duplicate
]

processor = SensorDataProcessor(expected_ranges)
cleaned_data = processor.validate_and_clean(sensor_data)
print(cleaned_data)