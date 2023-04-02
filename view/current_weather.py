from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import column, row
import os


class InfoDiv():
    def __init__(self, template, data='0'):
        self._template = template
        self.div = Div(text=self._template.format(data))
    
    def update(self, data):
        self.div.text = self._template.format(data)


class CurrentWeather():
    def __init__(self):
        self._create_view()

    def _create_view(self):     
        self._air_temp = InfoDiv('Air Temp: {}&deg;F')
        self._pressure = InfoDiv('Pressure: {} mb')
        self._humidity = InfoDiv('Humidity: {}%')
        self._ground_temp = InfoDiv('Gnd Temp: {}&deg;F')
        self._uv = InfoDiv('UV: {}')
        self._wind_speed = InfoDiv('Wind Speed: {} mph')
        self._gust = InfoDiv('Gust: {} mph')
        self._rainfall = InfoDiv('Rainfall: {} in')
        self._rain_rate = InfoDiv('Rain Rate: {} in/hr')
        
        row1 = row(self._air_temp.div, self._ground_temp.div, self._pressure.div, self._humidity.div)
        row2 = row(self._uv.div, self._wind_speed.div, self._gust.div, self._rainfall.div, self._rain_rate.div)
        self._cur_weather = column(row1, row2, sizing_mode='stretch_both')

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
        