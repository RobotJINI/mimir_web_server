from bokeh.models import ColumnDataSource, Range1d, DataRange1d, Legend, Label, DatetimeTickFormatter, BoxAnnotation, Span, HoverTool, Legend, LegendItem
from bokeh.plotting import figure
from model.theme import DefaultTheme
from bokeh.models.tools import WheelZoomTool, PanTool


class BasePlot:
    def __init__(self):
        self._plot = figure(x_axis_type='datetime', 
                            toolbar_location='above', 
                            tools=['pan', 'box_zoom', 'save', 'reset'], 
                            active_drag=None)
        
        self._plot.toolbar.autohide = True
        
        self._plot.x_range = DataRange1d(range_padding=0.0)
        self._plot.title.align = 'center'
        self._plot.title.text_font_size = '20pt'
        
        self._make_plot()
        
    def get_plot(self):
        return self._plot
    
    def _make_plot(self):
        pass

class HumidityPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            humidity=[5, 4, 6, 2, 1],
        ))
        self._plot.line(y='humidity', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        # Set initial y-axis range
        y_range = Range1d(start=0, end=100)
        self._plot.y_range = y_range
        
        self._plot.title.text = 'Humidity'
        
        hover_tool = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('Humidity', '@humidity{0.00}%')], 
            formatters={
                '@time': 'datetime'}, 
            mode='vline'
        )

        self._plot.add_tools(hover_tool)

    def update_plot(self, cds):
        if self._plot is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
            
            
class PressurePlot(BasePlot):
    def __init__(self):
        self._offset = 10
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            pressure=[5, 4, 6, 2, 1],
        ))
        self._plot.line(y='pressure', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        # Add dotted lines for upper and lower bounds
        self._plot.renderers.append(Span(location=6, dimension='width', line_color='green', line_dash='dashed'))
        self._plot.renderers.append(Span(location=1, dimension='width', line_color='red', line_dash='dashed'))
        self._plot.renderers.append(Span(location=3.5, dimension='width', line_color='blue', line_dash='dashed'))
        
        self._plot.title.text = 'Pressure (mbar)'
        
        hover_tool = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('Pressure', '@pressure{0.00} mbar')], 
            formatters={
                '@time': 'datetime'}, 
            mode='vline'
        )

        self._plot.add_tools(hover_tool)

    def update_plot(self, cds, lower_bound, upper_bound):
        if self._plot is not None:
            self._source.data.update(cds.data)
            
            # Update locations of dotted lines for upper and lower bounds
            self._plot.renderers[-3].location = upper_bound
            self._plot.renderers[-2].location = lower_bound
            self._plot.renderers[-1].location = (lower_bound + upper_bound) / 2
            
            # Update y-axis range
            new_y_range = Range1d(start=lower_bound - self._offset, 
                                  end=upper_bound + self._offset)
            self._plot.y_range = new_y_range
            self._plot.y_range.update()
        else:
            print("Error temp display module not initialized.")
            
            
class RainfallPlot(BasePlot):
    def __init__(self):
        self._offset = .25
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            rainfall=[5, 4, 6, 2, 1]
        ))
        self._plot.line(y='rainfall', x='time', source=self._source, color=DefaultTheme().get_default_line())

        self._plot.title.text = 'Rainfall (inch/hr)'
        
        hover_tool = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('Rain', '@rainfall{0.00} inch')], 
            formatters={
                '@time': 'datetime'}, 
            mode='vline'
        )

        self._plot.add_tools(hover_tool)

    def update_plot(self, cds):
        if self._plot is not None:
            self._source.data.update(cds.data)
            
            # Update y-axis range
            new_y_range = Range1d(start=0, 
                                  end=max(self._source.data['rainfall']) + self._offset)
            self._plot.y_range = new_y_range
            self._plot.y_range.update()
        else:
            print("Error temp display module not initialized.")
            
            
class TemperaturePlot(BasePlot):
    def __init__(self):
        self._offset = 10
        self._degree_char = '\u00b0'
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            air_temp=[5, 4, 6, 2, 1],
            ground_temp=[1, 2, 3, 5, 1]
        ))
        
        air_line = self._plot.line(y='air_temp', x='time', source=self._source, color=DefaultTheme().get_air(), legend_label='Air')
        gnd_line = self._plot.line(y='ground_temp', x='time', source=self._source, color=DefaultTheme().get_ground(), legend_label='Ground')
        
        self._plot.title.text = f'Temperature (F{self._degree_char})'
        self._plot.legend.location = 'top_left'
        
        hover_air = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('Air', '@air_temp{0.00} ' + f'F{self._degree_char}'),
                ('Gnd', '@ground_temp{0.00} ' + f'F{self._degree_char}')],
            formatters={
                '@time': 'datetime'},
            mode='vline',
            renderers=[air_line]
        )

        self._plot.add_tools(hover_air)

    def update_plot(self, cds):
        if self._plot is not None:
            self._source.data.update(cds.data)            
                        
            # Update y-axis range
            new_y_range = Range1d(start=min(self._source.data['air_temp']) - self._offset, 
                                  end=max(self._source.data['air_temp']) + self._offset)
            self._plot.y_range = new_y_range
            self._plot.y_range.update()
            
        else:
            print("Error temp display module not initialized.")
            
            
class UvPlot(BasePlot):
    def __init__(self):
        self._offset = 25
        self._default_end = 2500
        self._veml6070_risk_lv = {
                                    'LOW': [0, 560],
                                    'MODERATE': [561, 1120],
                                    'HIGH': [1121, 1494],
                                    'VERY HIGH': [1495, 2054],
                                    'EXTREME': [2055, 9999],
                                 }
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            uv=[5, 4, 6, 2, 1],
        ))
        
        self._plot.line(y='uv', x='time', source=self._source, color=DefaultTheme().get_default_line())
        
        # Define risk level boxes
        low_box = BoxAnnotation(bottom=self._veml6070_risk_lv['LOW'][0], top=self._veml6070_risk_lv['LOW'][1], fill_color='green', fill_alpha=0.2)
        moderate_box = BoxAnnotation(bottom=self._veml6070_risk_lv['MODERATE'][0], top=self._veml6070_risk_lv['MODERATE'][1], fill_color='#FFCC00', fill_alpha=0.2)
        high_box = BoxAnnotation(bottom=self._veml6070_risk_lv['HIGH'][0], top=self._veml6070_risk_lv['HIGH'][1], fill_color='orange', fill_alpha=0.2)
        very_high_box = BoxAnnotation(bottom=self._veml6070_risk_lv['VERY HIGH'][0], top=self._veml6070_risk_lv['VERY HIGH'][1], fill_color='red', fill_alpha=0.2)
        extreme_box = BoxAnnotation(bottom=self._veml6070_risk_lv['EXTREME'][0], top=self._veml6070_risk_lv['EXTREME'][1], fill_color='purple', fill_alpha=0.2)
        
        # Add boxes to the plot
        self._plot.add_layout(low_box)
        self._plot.add_layout(moderate_box)
        self._plot.add_layout(high_box)
        self._plot.add_layout(very_high_box)
        self._plot.add_layout(extreme_box)
        
        self._plot.title.text = 'UV (LOW)'
        
        hover_tool = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('UV', '@uv{0.00}')], 
            formatters={
                '@time': 'datetime'}, 
            mode='vline'
        )
        
        self._plot.add_tools(hover_tool)
        
    

    def update_plot(self, cds):
        if self._plot is not None:
            self._source.data.update(cds.data)
            
            self._plot.title.text = f'UV ({cds.data["uv_risk_lv"][0]})'
            
            # Update y-axis range
            end_range = self._default_end
            max_reading = max(self._source.data['uv'])
            if max_reading > self._default_end:
                end_range = max_reading + self._offset
            new_y_range = Range1d(start=0, 
                                  end=end_range)
            self._plot.y_range = new_y_range
            self._plot.y_range.update()
        else:
            print("Error temp display module not initialized.")
            
            
class WindSpeedPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def _make_plot(self):
        self._source = ColumnDataSource(data=dict(
            time=[1, 2, 3, 4, 5],
            wind_speed=[5, 4, 6, 2, 1],
        ))
        self._plot.line(y='wind_speed', x='time', source=self._source, color=DefaultTheme().get_default_line())

        self._plot.title.text = 'Wind Speed (mph)'
        
        hover_tool = HoverTool(
            tooltips=[
                ('Time', '@time{%F %T}'),
                ('Wind', '@wind_speed{0.00} mph')], 
            formatters={
                '@time': 'datetime'}, 
            mode='vline'
        )

        self._plot.add_tools(hover_tool)

    def update_plot(self, cds):
        if self._plot is not None:
            self._source.data.update(cds.data)
        else:
            print("Error temp display module not initialized.")
