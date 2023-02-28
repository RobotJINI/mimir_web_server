from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d


class PressureDisplay():
    def __init__(self):
        super().__init__()
        self._pressure_display = figure()
        #self._temp_display.y_range = Range1d(0, 40)

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            pressure=[5, 4, 6, 2, 1],
        ))
        self._pressure_display.line(y='pressure', x='time', source=self._source)
        return self._pressure_display

    def update_plot(self, dataframe):
        if self._pressure_display is not None:
            self._source.data.update(dataframe.data)
        else:
            print("Error temp display module not initialized.")
