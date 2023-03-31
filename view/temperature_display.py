from bokeh.models import ColumnDataSource, Range1d, DataRange1d, Legend, Label, DatetimeTickFormatter
from bokeh.plotting import figure
from model.theme import DefaultTheme


class TemperatureDisplay():
    def __init__(self):
        self._offset = 10
        self._degree_char = '\u00b0'
        self._temp_display = figure(x_axis_type="datetime")

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            air_temp=[5, 4, 6, 2, 1],
            ground_temp=[1, 2, 3, 5, 1]
        ))
        
        self._temp_display.line(y='air_temp', x='time', source=self._source, color=DefaultTheme().get_air(), legend_label='Air')
        self._temp_display.line(y='ground_temp', x='time', source=self._source, color=DefaultTheme().get_ground(), legend_label='Ground')
        
        self._temp_display.x_range = DataRange1d(range_padding=0.0)
        
        # Set initial y-axis range
        y_range = Range1d(start=min(self._source.data['air_temp'] + self._source.data['ground_temp']) - self._offset, 
                          end=max(self._source.data['air_temp'] + self._source.data['ground_temp']) + self._offset)
        self._temp_display.y_range = y_range

        self._temp_display.title.text = f'Temperature (F{self._degree_char})'
        self._temp_display.title.align = 'center'
        self._temp_display.title.text_font_size = '20pt'
        
        return self._temp_display

    def update_plot(self, cds):
        if self._temp_display is not None:
            self._source.data.update(cds.data)            
                        
            # Update y-axis range
            new_y_range = Range1d(start=min(self._source.data['air_temp']) - self._offset, 
                                  end=max(self._source.data['air_temp']) + self._offset)
            self._temp_display.y_range = new_y_range
            self._temp_display.y_range.update()
            
        else:
            print("Error temp display module not initialized.")
