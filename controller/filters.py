import pandas as pd
import numpy as np
from scipy.signal import savgol_filter


class CoreWeatherFilter:
    def __init__(self, window_size=400, polynomial=2):
        self._window_size = window_size
        self._polynomial = polynomial

    def process(self, data):
        return savgol_filter(data, self._window_size, self._polynomial)
    
class TimeFilter:
    def __init__(self):
        self._est_time_diff_msec = 3600000 * 5 #5 hours in milli seconds
        
    def process(self, data):
        data[:] = [self._to_est_seconds(time_ms) for time_ms in data]
        return data
    
    def _to_est_seconds(self, time_ms):
        return time_ms - self._est_time_diff_msec