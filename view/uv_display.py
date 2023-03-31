from bokeh.models import ColumnDataSource, Range1d, DataRange1d, BoxAnnotation
from bokeh.plotting import figure
from bokeh.models import Range1d
from model.theme import DefaultTheme

class UvDisplay():
    def __init__(self):
        self._uv_display = figure(x_axis_type="datetime")
        self._offset = 25
        self._default_end = 2500
        self._veml6070_risk_lv = {
                                    'LOW': [0, 560],
                                    'MODERATE': [561, 1120],
                                    'HIGH': [1121, 1494],
                                    'VERY HIGH': [1495, 2054],
                                    'EXTREME': [2055, 9999],
                                 }

    def make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            uv=[5, 4, 6, 2, 1],
        ))
        
        self._uv_display.line(y='uv', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        self._uv_display.x_range = DataRange1d(range_padding=0.0)
        
        # Define risk level boxes
        low_box = BoxAnnotation(bottom=self._veml6070_risk_lv['LOW'][0], top=self._veml6070_risk_lv['LOW'][1], fill_color='green', fill_alpha=0.2)
        moderate_box = BoxAnnotation(bottom=self._veml6070_risk_lv['MODERATE'][0], top=self._veml6070_risk_lv['MODERATE'][1], fill_color='#FFCC00', fill_alpha=0.2)
        high_box = BoxAnnotation(bottom=self._veml6070_risk_lv['HIGH'][0], top=self._veml6070_risk_lv['HIGH'][1], fill_color='orange', fill_alpha=0.2)
        very_high_box = BoxAnnotation(bottom=self._veml6070_risk_lv['VERY HIGH'][0], top=self._veml6070_risk_lv['VERY HIGH'][1], fill_color='red', fill_alpha=0.2)
        extreme_box = BoxAnnotation(bottom=self._veml6070_risk_lv['EXTREME'][0], top=self._veml6070_risk_lv['EXTREME'][1], fill_color='purple', fill_alpha=0.2)
        
        # Add boxes to the plot
        self._uv_display.add_layout(low_box)
        self._uv_display.add_layout(moderate_box)
        self._uv_display.add_layout(high_box)
        self._uv_display.add_layout(very_high_box)
        self._uv_display.add_layout(extreme_box)
        
        self._uv_display.title.text = 'UV (LOW)'
        self._uv_display.title.align = 'center'
        self._uv_display.title.text_font_size = '20pt'
        return self._uv_display

    def update_plot(self, cds):
        if self._uv_display is not None:
            self._source.data.update(cds.data)
            
            self._uv_display.title.text = f'UV ({cds.data["uv_risk_lv"][0]})'
            
            # Update y-axis range
            end_range = self._default_end
            max_reading = max(self._source.data['uv'])
            if max_reading > self._default_end:
                end_range = max_reading + self._offset
            new_y_range = Range1d(start=0, 
                                  end=end_range)
            self._uv_display.y_range = new_y_range
            self._uv_display.y_range.update()
        else:
            print("Error temp display module not initialized.")
