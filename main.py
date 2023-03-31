import time
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
from view.rainfall_display import RainfallDisplay
from controller.controllers import DisplayController
from bokeh.themes import Theme
import model.theme


class MimirWebServer:
    def __init__(self):
        self._theme = model.theme.DefaultTheme()
        self._build_ui()
        self.update()
        
    def _start_db_sync(self):
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def _build_ui(self):
        current_weather_module = CurrentWeather()
        current_weather_block = current_weather_module.make_plot('Updating....')

        temperature_display_module = TemperatureDisplay()
        temperature_display_block = temperature_display_module.make_plot()

        pressure_display_module = PressureDisplay()
        pressure_display_block = pressure_display_module.make_plot()

        humidity_display_module = HumidityDisplay()
        humidity_display_block = humidity_display_module.make_plot()

        uv_display_module = UvDisplay()
        uv_display_block = uv_display_module.make_plot()

        wind_speed_display_module = WindSpeedDisplay()
        wind_speed_display_block = wind_speed_display_module.make_plot()
        
        rainfall_display_module = RainfallDisplay()
        rainfall_display_block = rainfall_display_module.make_plot()
        
        self._display_controller = DisplayController(current_weather_module, temperature_display_module, 
                                                     pressure_display_module, humidity_display_module, 
                                                     uv_display_module, wind_speed_display_module, 
                                                     rainfall_display_module)

        curdoc().add_root(
            column(
                current_weather_block,
                row(temperature_display_block, pressure_display_block, humidity_display_block),
                row(uv_display_block, wind_speed_display_block, rainfall_display_block)
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
        

    def update(self):
         self._display_controller.update()


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
basicConfig()
mimir_web_server = MimirWebServer()
