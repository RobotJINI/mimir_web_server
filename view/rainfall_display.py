from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.plotting import figure
from model.theme import DefaultTheme

class RainfallDisplay():
    def __init__(self):
        self._rainfall = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            rainfall=[5, 4, 6, 2, 1]
        ))
        self._rainfall.line(y='rainfall', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._rainfall.x_range = DataRange1d(range_padding=0.0)

        self._rainfall.title.text = 'Rainfall (inch/hr)'
        self._rainfall.title.align = 'center'
        self._rainfall.title.text_font_size = '20pt'
        
        return self._rainfall

    def update_plot(self, cds):
        if self._rainfall is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
