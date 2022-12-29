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
        self.source = ColumnDataSource(data={})
        self.title = Paragraph(text="penis")
        self.data_table = DataTable(source=self.source, width=390, height=275, columns=[
            TableColumn(field="zipcode", title="Zipcodes", width=100),
            TableColumn(field="population", title="Population", width=100, formatter=NumberFormatter(format="0,0")),
            TableColumn(field="state_code", title="State")
        ])
        return column(self.title, self.data_table)

    def update_plot(self, dataframe):
        self.source.data.update(dataframe)

    def busy(self):
        self.title.text = 'Updating...'

    def unbusy(self):
        self.title.text = TITLE
