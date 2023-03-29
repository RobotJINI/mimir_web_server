from bokeh.models import ColumnDataSource, Range1d, DataRange1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from model.theme import DefaultTheme


class HumidityDisplay():
    def __init__(self):
        self._humidity_display = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            humidity=[5, 4, 6, 2, 1],
        ))
        self._humidity_display.line(y='humidity', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._humidity_display.x_range = DataRange1d(range_padding=0.0)
        
        self._humidity_display.title.text = 'Humidity'
        self._humidity_display.title.align = 'center'
        self._humidity_display.title.text_font_size = '20pt'
        
        return self._humidity_display

    def update_plot(self, cds):
        if self._humidity_display is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
