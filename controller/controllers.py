import threading
from controller.filters import CoreWeatherFilter, TimeFilter, RainFilter
from model.weather_database import WeatherDatabase
from model.weather_database_sync import WeatherDatabaseSync
from view.current_weather import CurrentWeather
from view.plots import HumidityPlot, PressurePlot, RainfallPlot, TemperaturePlot, UvPlot, WindSpeedPlot
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.layouts import column, row


class BasePlotController:
    def __init__(self):
        self._view = None
        
    def get_view(self):
        return self._view.get_plot()


class TemperatureController(BasePlotController):
    def __init__(self):
        self._view = TemperaturePlot()
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'air_temp': self._cwf.process(cds_dataframe.data['air_temp']),
                'ground_temp': self._cwf.process(cds_dataframe.data['ground_temp'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        

class PressureController(BasePlotController):
    def __init__(self, weather_db):
        self._view = PressurePlot()
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
        
            
class HumidityController(BasePlotController):
    def __init__(self):
        self._view = HumidityPlot()
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'humidity': self._cwf.process(cds_dataframe.data['humidity'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        

class UvController(BasePlotController):
    def __init__(self):
        self._view = UvPlot()
        self._cwf = CoreWeatherFilter()
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'uv': self._cwf.process(cds_dataframe.data['uv']),
                'uv_risk_lv': cds_dataframe.data['uv_risk_lv']
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        
        
class WindSpeedController(BasePlotController):
    def __init__(self):
        self._view = WindSpeedPlot()
        self._cwf = CoreWeatherFilter(window_size=800)
        
    def update(self, cds_dataframe):
        dict = {
                'time': cds_dataframe.data['time'],
                'wind_speed': self._cwf.process(cds_dataframe.data['wind_speed'])
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        

class RainController(BasePlotController):
    def __init__(self):
        self._view = RainfallPlot()
        self._rf = RainFilter()
        
    def update(self, cds_dataframe):
        rainfall, times = self._rf.process(cds_dataframe.data['rainfall'], cds_dataframe.data['time'])
        dict = {
                'time': times,
                'rainfall': rainfall
               }
        cds = ColumnDataSource(data=dict)
        self._view.update_plot(cds)
        
        
class DisplayController:
    def __init__(self):
        self._weather_db = WeatherDatabase()
        
        self._current_weather = CurrentWeather()
        
        self._plot_controllers = {
                                    'temp': TemperatureController(),
                                    'pressure': PressureController(self._weather_db),
                                    'humidity': HumidityController(),
                                    'uv': UvController(),
                                    'wind': WindSpeedController(),
                                    'rain': RainController()
                                 }
        
        self._view = column(
            self._current_weather.get_view(),
            row(self._plot_controllers['temp'].get_view(), self._plot_controllers['pressure'].get_view(), self._plot_controllers['humidity'].get_view()),
            row(self._plot_controllers['uv'].get_view(), self._plot_controllers['wind'].get_view(), self._plot_controllers['rain'].get_view()),
            sizing_mode='stretch_both'
            )
        
        self._tf = TimeFilter()
        
        self._db_sync = WeatherDatabaseSync()
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def update(self):
        cur_weather_resp = self._weather_db.get_current_weather() 
        self._current_weather.update(cur_weather_resp)
              
        hw_cds = self._weather_db.get_historical_weather(sub_sample=False)
        hw_cds.data['time'] = self._tf.process(hw_cds.data['time'])
        
        for controller in self._plot_controllers.values():
            controller.update(hw_cds)
            
    def view(self):
        return self._view
        
    def __del__(self):
        if self._db_sync_thread and self._db_sync_thread.is_alive():
            self._db_sync.stop()
            self._db_sync_thread.join()
        
        