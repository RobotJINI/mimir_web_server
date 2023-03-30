import pandas as pd
import numpy as np

class CoreWeatherFilter:
    def __init__(self, window_size=5, max_z_score=3):
        self._window_size = window_size
        self._max_z_score = max_z_score

    def process(self, data):
        return self._outlier_filter(pd.Series(data)).to_list()
    
    def _outlier_filter(self, data):
        # Identify outliers
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        outliers = z_scores > self._max_z_score
        
        local_avg = data.rolling(window=self._window_size, min_periods=1, center=True).mean()
        
        # Replace outliers with local average
        data[outliers] = local_avg[outliers]
        return data
    
class TimeFilter:
    def __init__(self):
        self._est_time_diff_msec = 3600000 * 5 #5 hours in milli seconds
        
    def process(self, data):
        data[:] = [self._to_est_seconds(time_ms) for time_ms in data]
        return data
    
    def _to_est_seconds(self, time_ms):
        return time_ms - self._est_time_diff_msec