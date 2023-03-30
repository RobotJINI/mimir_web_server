import threading
from controller.filters import HistoricalWeatherFilter, UpperLowerBoundsFilter
from model.weather_database import WeatherDatabase
from model.weather_database_sync import WeatherDatabaseSync

class DisplayController:
    def __init__(self, current_weather, temperature_display, pressure_display, humidity_display, uv_display, wind_speed_display):
        self._current_weather = current_weather
        self._temperature_display = temperature_display
        self._pressure_display = pressure_display
        self._humidity_display = humidity_display
        self._uv_display = uv_display
        self._wind_speed_display = wind_speed_display
        
        self._weather_db = WeatherDatabase()
        self._hwf = HistoricalWeatherFilter()
        self._ulbf = UpperLowerBoundsFilter()
        
        self._db_sync = WeatherDatabaseSync()
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def update(self):
        cur_weather_resp = self._weather_db.get_current_weather()       
        hw_cds = self._weather_db.get_historical_weather(sub_sample=False)
        hw_cds = self._hwf.process(hw_cds)

        self._current_weather.update_plot(cur_weather_resp)
        self._temperature_display.update_plot(hw_cds)
        
        self._update_pressure_display(hw_cds)
        
        self._humidity_display.update_plot(hw_cds)
        self._uv_display.update_plot(hw_cds)
        self._wind_speed_display.update_plot(hw_cds)
        
    def _update_pressure_display(self, hw_cds):
        upper_bounds, lower_bounds = self._weather_db.get_upper_lower_bounds()
        upper_bound, lower_bound = self._ulbf.process(upper_bounds, lower_bounds)
        self._pressure_display.update_plot(hw_cds, upper_bound, lower_bound)
        
    def __del__(self):
        if self._db_sync_thread and self._db_sync_thread.is_alive():
            self._db_sync.stop()
            self._db_sync_thread.join()
        
    
    