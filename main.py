import concurrent
import time
import threading
import logging
from utils.utils import get_time_ms

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Paragraph

from modules.current_weather import CurrentWeather
from modules.temperature_display import TemperatureDisplay
from modules.humidity_display import HumidityDisplay
from modules.pressure_display import PressureDisplay
from modules.uv_display import UvDisplay
from modules.wind_speed_display import WindSpeedDisplay
from model.server_db import WeatherDatabase, WeatherDatabaseSync


class MimirWebServer:
    def __init__(self):
        self._weather_db = WeatherDatabase()
        self._db_sync = WeatherDatabaseSync()
        self._db_sync_thread = None

        self._start_db_sync()
        self._build_ui()
        self.update()
        
    def _start_db_sync(self):
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def _build_ui(self):
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
        
    def __del__(self):
        if self._db_sync_thread and self._db_sync_thread.is_alive():
            self._db_sync.stop()
            self._db_sync_thread.join()
        

    def update(self):
        cur_weather_resp = self._weather_db.get_current_weather()       
        measurement_df = self._weather_db.get_historical_weather()

        self._current_weather_module.update_plot(cur_weather_resp)
        self._temperature_display_module.update_plot(measurement_df)
        self._pressure_display_module.update_plot(measurement_df)
        self._humidity_display_module.update_plot(measurement_df)
        self._uv_display_module.update_plot(measurement_df)
        self._wind_speed_display_module.update_plot(measurement_df)
        logging.debug(f'response:{cur_weather_resp}')


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
mimir_web_server = MimirWebServer()
