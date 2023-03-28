from filters.filters import ToPdSeriesFilter, OutliersFilter, ToListFilter
from filters.filters import ToEstFilter

class CoreWeatherFilterChain:
    def __init__(self):
        self.filter_chain = ToPdSeriesFilter()
        self.filter_chain.set_next(OutliersFilter())
        self.filter_chain.set_next(ToListFilter())

    def process(self, data):
        return self.filter_chain.process(data)
    
class TimeFilterChain:
    def __init__(self):
        self.filter_chain = ToEstFilter()
        
    def process(self, data):
        return self.filter_chain.process(data)

class HistoricalWeatherFilter():
    def __init__(self):
        self._cwfc = CoreWeatherFilterChain()
        self._tfc = TimeFilterChain()
        
    def process(self, cds_dataframe):
        cds_dataframe.data['time'] = self._tfc.process(cds_dataframe.data['time'])
        
        cds_dataframe.data['air_temp'] = self._cwfc.process(cds_dataframe.data['air_temp'])
        cds_dataframe.data['pressure'] = self._cwfc.process(cds_dataframe.data['pressure'])
        cds_dataframe.data['humidity'] = self._cwfc.process(cds_dataframe.data['humidity'])
        cds_dataframe.data['ground_temp'] = self._cwfc.process(cds_dataframe.data['ground_temp'])
        return cds_dataframe