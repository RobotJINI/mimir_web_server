from bokeh.models import ColumnDataSource, Range1d, Span
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column
from bokeh.plotting import figure
from model.theme import DefaultTheme
from bokeh.models import DataRange1d


class PressureDisplay():
    def __init__(self):
        super().__init__()
        self._pressure_display = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            pressure=[5, 4, 6, 2, 1],
        ))
        self._pressure_display.line(y='pressure', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._pressure_display.x_range = DataRange1d(range_padding=0.0)
        
        # Add dotted lines for upper and lower bounds
        self._pressure_display.add_layout(Span(location=6, dimension='width', line_color='green', line_dash='dashed'))
        self._pressure_display.add_layout(Span(location=1, dimension='width', line_color='red', line_dash='dashed'))
        
        self._pressure_display.title.text = 'Pressure (mbar)'
        self._pressure_display.title.align = 'center'
        self._pressure_display.title.text_font_size = '20pt'
        return self._pressure_display

    def update_plot(self, cds, upper_bound, lower_bound):
        if self._pressure_display is not None:
            self._source.data.update(cds.data)
            
            # Update locations of dotted lines for upper and lower bounds
            print(len(self._pressure_display.renderers))
            #self._pressure_display.renderers[-2].location = upper_bound
            #self._pressure_display.renderers[-1].location = lower_bound
        else:
            print("Error temp display module not initialized.")
