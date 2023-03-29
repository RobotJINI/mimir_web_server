import time
import logging
from model.weather_database import WeatherDatabase
from model.weather_grpc_client import WeatherGrpcClient
from utils.utils import get_time_ms

class WeatherDatabaseSync:
    def __init__(self):
        self._weather_grpc_client = WeatherGrpcClient(hostname='mimir.local')
        self._weather_db = WeatherDatabase()
        self._running = False
        self._interval = 10000
        self._last_updated_time = None
        
    def run(self):
        self._running = True
        while(self._running):
            time_ms = get_time_ms()
            if self._last_updated_time is None or (time_ms - self._last_updated_time) >= self._interval:
                self._update()
                self._last_updated_time = time_ms

            time.sleep(.1)
            
        
    def stop(self):
        self._running = False
        
    def _update(self):
        start_time = self._weather_db.get_last_entry_time()
        end_time = get_time_ms()
        logging.debug(f'self._weather_grpc_client.get_measurements(start_time={start_time}, end_time={end_time})')
        measurement_pb = self._weather_grpc_client.get_measurements(start_time, end_time)
        
        for measurement in measurement_pb.measurements:
            self._weather_db.insert(measurement.time, measurement.air_temp, measurement.pressure, measurement.humidity, measurement.ground_temp, measurement.uv,
                                    measurement.uv_risk_lv, measurement.wind_speed, measurement.rainfall, measurement.rain_rate, measurement.wind_dir)