from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d


class HumidityDisplay():
    def __init__(self):
        super().__init__()
        self._humidity_display = figure()
        #self._temp_display.y_range = Range1d(0, 40)

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            humidity=[5, 4, 6, 2, 1],
        ))
        self._humidity_display.line(y='humidity', x='time', source=self._source)
        return self._humidity_display

    def update_plot(self, dataframe):
        if self._humidity_display is not None:
            self._source.data.update(dataframe.data)
        else:
            print("Error temp display module not initialized.")
