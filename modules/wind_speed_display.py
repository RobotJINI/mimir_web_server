from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d


class WindSpeedDisplay():
    def __init__(self):
        super().__init__()
        self._wind_speed_display = figure()
        #self._temp_display.y_range = Range1d(0, 40)

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            wind_speed=[5, 4, 6, 2, 1],
        ))
        self._wind_speed_display.line(y='wind_speed', x='time', source=self._source)
        return self._wind_speed_display

    def update_plot(self, dataframe):
        if self._wind_speed_display is not None:
            self._source.data.update(dataframe.data)
        else:
            print("Error temp display module not initialized.")
