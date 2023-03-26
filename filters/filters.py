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
    
    
class CoreWeatherFilterChain:
    def __init__(self):
        self.filter_chain = ToPdSeriesFilter()
        self.filter_chain.set_next(OutliersFilter())
        self.filter_chain.set_next(ToListFilter())

    def process(self, data):
        return self.filter_chain.process(request)
