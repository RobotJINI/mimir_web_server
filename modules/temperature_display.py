from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.models import DatetimeTickFormatter
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d


class TemperatureDisplay():
    def __init__(self):
        super().__init__()
        self._temp_display = figure(x_axis_type="datetime")
        #self._temp_display.y_range = Range1d(0, 40)

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            air_temp=[5, 4, 6, 2, 1],
            ground_temp=[1, 2, 3, 5, 1]
        ))
        self._temp_display.line(y='air_temp', x='time', source=self._source)
        self._temp_display.line(y='ground_temp', x='time', source=self._source)
        return self._temp_display

    def update_plot(self, cds):
        if self._temp_display is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
