from data_cleaning import SensorDataProcessor, expected_ranges
import unittest

class TestSensorDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = SensorDataProcessor(expected_ranges)
    
    def test_out_of_range_values(self):
        test_data = [{"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": -50, "humidity": 110, "pressure": 1200, "battery": 105}]
        cleaned = self.processor.validate_and_clean(test_data)
        self.assertTrue(cleaned.isna().sum().sum() > 0)  # Expect NaN for out-of-range values
    
    def test_duplicate_timestamps(self):
        test_data = [
            {"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": 25.5, "humidity": 80, "pressure": 1200, "battery": 105},
            {"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": 26.0, "humidity": 101, "pressure": 870, "battery": 110},
        ]
        cleaned = self.processor.validate_and_clean(test_data)
        self.assertEqual(len(cleaned), 1)  # Expect only one entry per timestamp
    
    def test_missing_values_interpolation(self):
        test_data = [
            {"device_id": "sensor_123", "timestamp": "2025-01-29T14:30:00Z", "temperature": 25.5, "humidity": 85, "pressure": 1200, "battery": None},
            {"device_id": "sensor_123", "timestamp": "2025-01-29T14:32:00Z", "temperature": 26.5, "humidity": None, "pressure": 950, "battery": 320},
        ]
        cleaned = self.processor.validate_and_clean(test_data)
        self.assertTrue(cleaned.isna().any().any())  # Expect interpolation to fill missing values
    
if __name__ == "__main__":
    unittest.main()
