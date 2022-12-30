import concurrent
import time

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Paragraph

import modules.current_weather
from grpclient.client import WeatherGrpcClient


class MimirWebServer:
    def __init__(self):
        self._weather_grpc_client = WeatherGrpcClient()
        
        self._current_weather_module = modules.current_weather.CurrentWeather()
        self._current_weather_block = getattr(self._current_weather_module, 'make_plot')({})
        
        curdoc().add_root(
            column(
                row(column(self._current_weather_block))
                )
            )
        
        curdoc().add_periodic_callback(self.update, 5000)
        curdoc().title = "Mimir Weather Station"
        
    def update(self):
        self._weather_grpc_client.get_update()
        
        
mimir_web_server = MimirWebServer()
