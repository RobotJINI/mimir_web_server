from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import column
import os


class CurrentWeather():
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../templates/current_weather.html'), 'r') as f:
            self._template = f.read()
        self._create_view()

    def _create_view(self):
        default_data = {'air_temp': '48.64', 
                        'pressure': '1010.74', 
                        'humidity': '26.40', 
                        'ground_temp': '44.27', 
                        'uv': '237.7', 
                        'wind_speed': '1.64', 
                        'gust': '2.54', 
                        'rainfall': '0E-8', 
                        'rain_rate': '0E-8'}
        html = self._template.format(**default_data)
        self._cur_weather = Div(text=html)

    def get_view(self):
        return self._cur_weather

    def update(self, dataframe):
        html = self._template.format(**dataframe)
        self._cur_weather.text = html