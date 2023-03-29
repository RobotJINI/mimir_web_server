import pandas as pd
import numpy as np

class Filter:
    def __init__(self):
        self.next_filter = None

    def process(self, data):
        if self.next_filter is None:
            return data

        return self.next_filter.process(data)

    def set_next(self, filter):
        self.next_filter = filter
        
        
class ToPdSeriesFilter(Filter):
    def process(self, data):
        return super().process(pd.Series(data))
    
class ToListFilter(Filter):
    def process(self, data):
        return super().process(data.to_list())
    
#expects time list in ms
class ToEstFilter(Filter):
    def __init__(self):
        super().__init__()
        self._est_time_diff_msec = 3600000 * 5 #5 hours in milli seconds
        
    def process(self, data):
        data[:] = [self._to_est_seconds(time_ms) for time_ms in data]
        return super().process(data)
    
    def _to_est_seconds(self, time_ms):
        return time_ms - self._est_time_diff_msec
    
    
class OutliersFilter(Filter):
    def __init__(self, window_size=5, max_z_score=3):
        self._window_size = window_size
        self._max_z_score = max_z_score
        super().__init__()
        
    def process(self, data):
        # Identify outliers
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        outliers = z_scores > max_z_score
        
        local_avg = data.rolling(window=window_size, min_periods=1, center=True).mean()
        
        # Replace outliers with local average
        data[outliers] = local_avg[outliers]
        return super().process(data)
    
class MeanFilter(Filter):
    def process(self, data):
        return super().process(np.mean(data))
