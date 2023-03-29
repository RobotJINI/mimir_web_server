import concurrent
import time
import threading
import logging
from utils.utils import get_time_ms

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Paragraph
from bokeh.util.logconfig import basicConfig

from view.current_weather import CurrentWeather
from view.temperature_display import TemperatureDisplay
from view.humidity_display import HumidityDisplay
from view.pressure_display import PressureDisplay
from view.uv_display import UvDisplay
from view.wind_speed_display import WindSpeedDisplay
from model.weather_database_sync import WeatherDatabaseSync
from model.weather_database import WeatherDatabase
from filters.historical_weather_filter import HistoricalWeatherFilter
from filters.upper_lower_bounds_filter import UpperLowerBoundsFilter
from bokeh.themes import Theme
import model.theme


class MimirWebServer:
    def __init__(self):
        self._weather_db = WeatherDatabase()
        self._db_sync = WeatherDatabaseSync()
        self._db_sync_thread = None
        self._theme = model.theme.DefaultTheme()

        self._start_db_sync()
        self._build_ui()
        self._hwf = HistoricalWeatherFilter()
        self._ulbf = UpperLowerBoundsFilter()
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
        
        #self._add_custom_theme()
        
        
    def _add_custom_theme(self):
        # define a custom theme with a light blue background
        custom_theme = Theme(
            json={
                'attrs': {
                    'Figure': {
                        'background_fill_color': self._theme.get_background_fill()
                    }
                }
            }
        )
        
        # apply the custom theme to the current document
        curdoc().theme = custom_theme
        
    def __del__(self):
        if self._db_sync_thread and self._db_sync_thread.is_alive():
            self._db_sync.stop()
            self._db_sync_thread.join()
        

    def update(self):
        cur_weather_resp = self._weather_db.get_current_weather()       
        hw_cds = self._weather_db.get_historical_weather(sub_sample=True)
        hw_cds = self._hwf.process(hw_cds)

        self._current_weather_module.update_plot(cur_weather_resp)
        self._temperature_display_module.update_plot(hw_cds)
        
        self._update_pressure_display(hw_cds)
        
        self._humidity_display_module.update_plot(hw_cds)
        self._uv_display_module.update_plot(hw_cds)
        self._wind_speed_display_module.update_plot(hw_cds)
        logging.debug(f'response:{cur_weather_resp}')
        
    def _update_pressure_display(self, hw_cds):
        upper_bounds, lower_bounds = self._weather_db.get_upper_lower_bounds()
        upper_bound, lower_bound = self._ulbf.process(upper_bounds, lower_bounds)
        self._pressure_display_module.update_plot(hw_cds, upper_bound, lower_bound)


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
basicConfig()
mimir_web_server = MimirWebServer()
