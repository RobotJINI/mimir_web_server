from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import grid, row, column
import os


class InfoDiv():
    def __init__(self, label, input_template, inner=True, data='0'):
        div_width = 275 if inner else 550
        label_width = 180 if inner else 415
        self._label_style = f'"font-weight: bold; margin-right: 5px; display: inline-block; width: {label_width}px;"'
        self._value_style = f'"display: inline-block; text-align: right; width: {div_width - label_width}px;"'
        self._template = input_template
        div_styles = {'width': f'{div_width}px', 'padding': '5px'}
        if not inner:
            div_styles['border-bottom'] = '1px solid gray'
            
        label_row = row(Div(text=label, styles={'font-weight': 'bold', 'margin-right': '5px', 'width': f'{label_width}px'}))
        self._value_div = Div(text=input_template, sizing_mode='stretch_width', styles={'text-align': 'right'})
        value_row = row(self._value_div)
        self.div = row(label_row, value_row, styles=div_styles)
    
    def update(self, data):
        self._value_div.text = self._template.format(data)


class CurrentWeather():
    def __init__(self):
        self._create_view()

    def _create_view(self):   
        self._header = InfoDiv('Current Weather', '{}', inner=False)  
        self._air_temp = InfoDiv('Air Temp', '{}&deg;F')
        self._pressure = InfoDiv('Pressure', '{} mb')
        self._humidity = InfoDiv('Humidity', '{}%')
        self._ground_temp = InfoDiv('Gnd Temp', '{}&deg;F')
        self._uv = InfoDiv('UV', '{}')
        self._wind_speed = InfoDiv('Wind', '{} mph')
        self._gust = InfoDiv('Gust', '{} mph')
        self._rainfall = InfoDiv('Rainfall', '{} in')
        self._rain_rate = InfoDiv('Rain Rate', '{} in/hr')
        
        info_grid = grid([self._air_temp.div, self._ground_temp.div, self._pressure.div, self._humidity.div, 
                          self._uv.div, self._wind_speed.div, self._gust.div, self._rainfall.div, self._rain_rate.div], 
                          ncols=2, sizing_mode='stretch_width')
        inner_table = column(self._header.div, info_grid, styles={'border': '1px solid gray', 'border-style': 'outset', 'background-color': 'lightblue'})
        table_background = column(inner_table, align='center', sizing_mode='stretch_height', styles={'background': '#E0E0E2', 'border-style': 'inset', 'border': '1px solid gray'})
        self._cur_weather = column(table_background, align='center', sizing_mode='stretch_height', styles={'padding': '35px 0', 'padding-left': '25px'})

    def get_view(self):
        return self._cur_weather

    def update(self, dataframe):
        self._header.update(dataframe['time'])
        self._air_temp.update(dataframe['air_temp'])
        self._pressure.update(dataframe['pressure'])
        self._humidity.update(dataframe['humidity'])
        self._ground_temp.update(dataframe['ground_temp'])
        self._uv.update(dataframe['uv'])
        self._wind_speed.update(dataframe['wind_speed'])
        self._gust.update(dataframe['gust'])
        self._rainfall.update(dataframe['rainfall'])
        self._rain_rate.update(dataframe['rain_rate'])
        