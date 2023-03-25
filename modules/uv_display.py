from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import Range1d


class UvDisplay():
    def __init__(self):
        super().__init__()
        self._uv_display = figure()
        #self._temp_display.y_range = Range1d(0, 40)

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            uv=[5, 4, 6, 2, 1],
        ))
        self._uv_display.line(y='uv', x='time', source=self._source)
        return self._uv_display

    def update_plot(self, cds):
        if self._uv_display is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
