import pandas as pd
import numpy as np
import datetime
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
    

class RainFilter:
    def __init__(self):
        self._mm_per_inch = 25.4
        
    def process(self, rainfall, times):
        # Create lists to store rainfall data per hour and new times
        rainfall_per_hour = []
        times_per_hour = []
        
        # Iterate over input data
        for i in range(len(rainfall)):
            # Convert epoch time to datetime object
            dt = datetime.datetime.fromtimestamp(times[i] / 1000)
            # Round down to the nearest hour
            hour = dt.replace(minute=0, second=0, microsecond=0)
            # Add rainfall data to list
            if not rainfall_per_hour or times_per_hour[-1] != hour:
                rainfall_per_hour.append(rainfall[i])
                times_per_hour.append(hour)
            else:
                rainfall_per_hour[-1] += rainfall[i]
                
        #convert back to ms since epoch
        times_per_hour[:] = [x.timestamp() * 1000 for x in times_per_hour]
        
        #convert to inches from mm
        rainfall_per_hour[:] = [x / self._mm_per_inch for x in rainfall_per_hour]
        return rainfall_per_hour, times_per_hour
    

class CurrentWeatherFilter:
    def __init__(self, precision=1):
        self._precision = precision
        
    def process(self, dataframe):
        for key in dataframe:
            if dataframe[key] is None:
                dataframe[key] = 0.0
            else:
                dataframe[key] = round(float(dataframe[key]), self._precision)
        return dataframe