from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d
from model.theme import DefaultTheme


class WindSpeedDisplay():
    def __init__(self):
        self._wind_speed_display = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            wind_speed=[5, 4, 6, 2, 1],
        ))
        self._wind_speed_display.line(y='wind_speed', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._wind_speed_display.x_range = DataRange1d(range_padding=0.0)

        self._wind_speed_display.title.text = 'Wind Speed (mph)'
        self._wind_speed_display.title.align = 'center'
        self._wind_speed_display.title.text_font_size = '20pt'
        
        return self._wind_speed_display

    def update_plot(self, cds):
        if self._wind_speed_display is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
