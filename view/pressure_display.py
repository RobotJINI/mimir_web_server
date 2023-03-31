from bokeh.models import ColumnDataSource, Range1d, Span, DataRange1d
from bokeh.plotting import figure
from model.theme import DefaultTheme


class PressureDisplay():
    def __init__(self):
        self._offset = 10
        self._pressure_display = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            pressure=[5, 4, 6, 2, 1],
        ))
        self._pressure_display.line(y='pressure', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._pressure_display.x_range = DataRange1d(range_padding=0.0)
        
        # Add dotted lines for upper and lower bounds
        self._pressure_display.renderers.append(Span(location=6, dimension='width', line_color='green', line_dash='dashed'))
        self._pressure_display.renderers.append(Span(location=1, dimension='width', line_color='red', line_dash='dashed'))
        self._pressure_display.renderers.append(Span(location=3.5, dimension='width', line_color='blue', line_dash='dashed'))
        
        self._pressure_display.title.text = 'Pressure (mbar)'
        self._pressure_display.title.align = 'center'
        self._pressure_display.title.text_font_size = '20pt'
        return self._pressure_display

    def update_plot(self, cds, lower_bound, upper_bound):
        if self._pressure_display is not None:
            self._source.data.update(cds.data)
            
            # Update locations of dotted lines for upper and lower bounds
            self._pressure_display.renderers[-3].location = upper_bound
            self._pressure_display.renderers[-2].location = lower_bound
            self._pressure_display.renderers[-1].location = (lower_bound + upper_bound) / 2
            
            # Update y-axis range
            new_y_range = Range1d(start=lower_bound - self._offset, 
                                  end=upper_bound + self._offset)
            self._pressure_display.y_range = new_y_range
            self._pressure_display.y_range.update()
        else:
            print("Error temp display module not initialized.")
