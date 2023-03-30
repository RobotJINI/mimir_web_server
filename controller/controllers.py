import threading
from controller.filters import CoreWeatherFilter, TimeFilter
from model.weather_database import WeatherDatabase
from model.weather_database_sync import WeatherDatabaseSync
import numpy as np
from bokeh.models import ColumnDataSource


class TemperatureController:
    def __init__(self, view):
        self._view = view
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'air_temp': self._cwf.process(cds_dataframe.data['air_temp']),
                'ground_temp': self._cwf.process(cds_dataframe.data['ground_temp'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        

class PressureController:
    def __init__(self, view, weather_db):
        self._view = view
        self._weather_db = weather_db
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        upper_bounds, lower_bounds = self._weather_db.get_upper_lower_bounds()
        
        dict = {
                'time': cds_dataframe.data['time'],
                'pressure': self._cwf.process(cds_dataframe.data['pressure'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds, np.mean(lower_bounds), np.mean(upper_bounds))
        
            
class HumidityController:
    def __init__(self, view):
        self._view = view
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'humidity': self._cwf.process(cds_dataframe.data['humidity'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        

class UvController:
    def __init__(self, view):
        self._view = view
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'uv': self._cwf.process(cds_dataframe.data['uv']),
                'uv_risk_lv': cds_dataframe.data['uv_risk_lv']
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        
        
class WindSpeedController:
    def __init__(self, view):
        self._view = view
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'wind_speed': self._cwf.process(cds_dataframe.data['wind_speed'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)    
        
        
class DisplayController:
    def __init__(self, current_weather, temperature_display, pressure_display, humidity_display, uv_display, wind_speed_display):
        self._weather_db = WeatherDatabase()
        
        self._current_weather = current_weather
        self._temperature_controller = TemperatureController(temperature_display)
        self._pressure_controller = PressureController(pressure_display, self._weather_db)
        self._humidity_controller = HumidityController(humidity_display)
        self._uv_controller = UvController(uv_display)
        self._wind_speed_controller = WindSpeedController(wind_speed_display)
        
        self._tf = TimeFilter()
        
        self._db_sync = WeatherDatabaseSync()
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def update(self):
        cur_weather_resp = self._weather_db.get_current_weather() 
        self._current_weather.update_plot(cur_weather_resp)
              
        hw_cds = self._weather_db.get_historical_weather(sub_sample=False)
        hw_cds.data['time'] = self._tf.process(hw_cds.data['time'])
        
        self._temperature_controller.update(hw_cds)
        self._pressure_controller.update(hw_cds)
        self._humidity_controller.update(hw_cds)
        self._uv_controller.update(hw_cds)
        self._wind_speed_controller.update(hw_cds)
        
    def __del__(self):
        if self._db_sync_thread and self._db_sync_thread.is_alive():
            self._db_sync.stop()
            self._db_sync_thread.join()
        
        