from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import grid
import os


class InfoDiv():
    def __init__(self, label, input_template, data='0'):
        self._template = self._create_template(label, input_template)
        self.div = Div(text=self._template.format(data), flow_mode='inline', 
                       styles={'font-size': '20px', 'text-align': 'center', 'padding': '10px', 
                               'border-bottom': '1px solid gray', 'display': 'inline-flex',
                               'justify-content': 'space-between', 'width': '100%'})
    
    def update(self, data):
        self.div.text = self._template.format(data)
        
    def _create_template(self, label, input_template):
        return f'<div>{label}</div><div>{input_template}</div>'


class CurrentWeather():
    def __init__(self):
        self._create_view()

    def _create_view(self):     
        self._air_temp = InfoDiv('Air Temp:', '{}&deg;F')
        self._pressure = InfoDiv('Pressure:', '{} mb')
        self._humidity = InfoDiv('Humidity:', '{}%')
        self._ground_temp = InfoDiv('Gnd Temp:', '{}&deg;F')
        self._uv = InfoDiv('UV:', '{}')
        self._wind_speed = InfoDiv('Wind Speed:', '{} mph')
        self._gust = InfoDiv('Gust:', '{} mph')
        self._rainfall = InfoDiv('Rainfall:', '{} in')
        self._rain_rate = InfoDiv('Rain Rate:', '{} in/hr')
        
        self._cur_weather = grid([self._air_temp.div, self._ground_temp.div, self._pressure.div, self._humidity.div, 
                                  self._uv.div, self._wind_speed.div, self._gust.div, self._rainfall.div, self._rain_rate.div], 
                                  ncols=2)

    def get_view(self):
        return self._cur_weather

    def update(self, dataframe):
        self._air_temp.update(dataframe['air_temp'])
        self._pressure.update(dataframe['pressure'])
        self._humidity.update(dataframe['humidity'])
        self._ground_temp.update(dataframe['ground_temp'])
        self._uv.update(dataframe['uv'])
        self._wind_speed.update(dataframe['wind_speed'])
        self._gust.update(dataframe['gust'])
        self._rainfall.update(dataframe['rainfall'])
        self._rain_rate.update(dataframe['rain_rate'])
        