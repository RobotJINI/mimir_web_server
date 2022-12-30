import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column

from modules.base import ModuleBase


class CurrentWeather(ModuleBase):

    def __init__(self):
        super().__init__()
        self.source = None
        self.data_table = None
        self.title = None
        
    def make_plot(self, dataframe):
        self.cur_weather = Paragraph(text=f'{dataframe}')
        return self.cur_weather

    def update_plot(self, dataframe):
        self.cur_weather.text = f'{dataframe}'

    def busy(self):
        pass

    def unbusy(self):
        pass
