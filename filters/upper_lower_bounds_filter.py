from filters.filters import ToPdSeriesFilter, OutliersFilter, MeanFilter


class MeanBoundsFilterChain:
    def __init__(self):
        self.filter_chain = ToPdSeriesFilter()
        self.filter_chain.set_next(OutliersFilter())
        self.filter_chain.set_next(MeanFilter())
        
    def process(self, data):
        return self.filter_chain.process(data)

class UpperLowerBoundsFilter():
    def __init__(self):
       self._mbfc = MeanBoundsFilterChain()
       
    def process(self, upper_bounds, lower_bounds):
        upper_bound = self._mbfc.process(upper_bounds)
        lower_bound = self._mbfc.process(lower_bounds)
        return(upper_bound, lower_bound)