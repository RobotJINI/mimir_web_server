import concurrent
import time

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Paragraph

from modules.current_weather import CurrentWeather
from modules.temperature_display import TemperatureDisplay
from modules.humidity_display import HumidityDisplay
from modules.pressure_display import PressureDisplay
from modules.uv_display import UvDisplay
from modules.wind_speed_display import WindSpeedDisplay
from grpclient.client import WeatherGrpcClient


class MimirWebServer:
    def __init__(self):
        self._weather_grpc_client = WeatherGrpcClient(ip='192.168.10.179')

        self._current_weather_module = CurrentWeather()
        self._current_weather_block = self._current_weather_module.make_plot('Updating....')

        self._temperature_display_module = TemperatureDisplay()
        self._temperature_display_block = self._temperature_display_module.make_plot()

        self._pressure_display_module = PressureDisplay()
        self._pressure_display_block = self._pressure_display_module.make_plot()

        self._humidity_display_module = HumidityDisplay()
        self._humidity_display_block = self._humidity_display_module.make_plot()

        self._uv_display_module = UvDisplay()
        self._uv_display_block = self._uv_display_module.make_plot()

        self._wind_speed_display_module = WindSpeedDisplay()
        self._wind_speed_display_block = self._wind_speed_display_module.make_plot()

        curdoc().add_root(
            column(
                self._current_weather_block,
                row(self._temperature_display_block, self._pressure_display_block, self._humidity_display_block),
                row(self._uv_display_block, self._wind_speed_display_block)
                )
            )

        curdoc().add_periodic_callback(self.update, 5000)
        curdoc().title = "Mimir Weather Station"

    def update(self):
        response = self._weather_grpc_client.get_current_weather()
        measurement_df = self._weather_grpc_client.get_measurements()

        self._current_weather_module.update_plot(response)
        self._temperature_display_module.update_plot(measurement_df)
        self._pressure_display_module.update_plot(measurement_df)
        self._humidity_display_module.update_plot(measurement_df)
        self._uv_display_module.update_plot(measurement_df)
        self._wind_speed_display_module.update_plot(measurement_df)
        print(f'response:{response}')


mimir_web_server = MimirWebServer()
