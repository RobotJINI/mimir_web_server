import MySQLdb, datetime, http.client, json, os
import io
import time
import math
import logging
import threading
from grpclient.weather_grpc_client import WeatherGrpcClient


class MysqlDatabase:
    def __init__(self, credentials):
        self._credentials = credentials

    def execute(self, query, params=[]):
        try:
            connection = MySQLdb.connect(user=self._credentials["USERNAME"], password=self._credentials["PASSWORD"], database=self._credentials["DATABASE"])
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            connection.close()
        except Exception as e:
            connection.rollback()
            connection.close()
            logging.error(f'Failed to execute query: {query} with params {params}. Error: {e}')
            raise

    def query(self, query, params=[]):
        try:
            connection = MySQLdb.connect(user=self._credentials["USERNAME"], password=self._credentials["PASSWORD"], database=self._credentials["DATABASE"])
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.close()
            return result
        except Exception as e:
            connection.close()
            logging.error(f'Failed to execute query: {query} with params {params}. Error: {e}')
            raise


class WeatherDatabase:
    def __init__(self):
        self._insert_template = 'INSERT INTO weather_measurement (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, ' + \
                                'rain_rate, wind_dir) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                                
        self._latest_time_template = 'SELECT * FROM weather_measurement ORDER BY time DESC LIMIT 1;'

                                          
        credentials_file = os.path.join(os.path.dirname(__file__), "../config/credentials.mysql")                                  
        self._credentials = self._load_credentials(credentials_file)
        self._db = MysqlDatabase(self._credentials)
                                          
    def _load_credentials(self, credentials_file):
        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            for key, value in credentials.items():
                credentials[key] = value.strip()  # remove leading/trailing whitespace
            return credentials
        except FileNotFoundError:
            logging.error(f'Credentials file \'{credentials_file}\' does not exist. Creating a new one, please modify password...')
            with open(credentials_file, 'w') as f:
                credentials = {'USERNAME': 'admin', 'PASSWORD': '*******', 'DATABASE': 'weather'}
                json.dump(credentials, f)
            sys.exit(1)

    def insert(self, time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir):
        params = (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir)
        logging.debug(self._insert_template % params)
        self._db.execute(self._insert_template, params)
    
    def get_last_entry_time(self):
        return self._db.query(self._latest_time_template)[0]['time'] + 1
    
    
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
            time_ms = self._get_time_ms()
            if self._last_updated_time is None or (time_ms - self._last_updated_time) >= self._interval:
                self._update()
                self._last_updated_time = time_ms

            time.sleep(.1)
            
        
    def stop(self):
        self._running = False
        
    def _update(self):
        start_time = self._weather_db.get_last_entry_time()
        end_time = self._get_time_ms()
        logging.debug(f'self._weather_grpc_client.get_measurements(start_time={start_time}, end_time={end_time})')
        measurement_pb = self._weather_grpc_client.get_measurements(start_time=start_time, end_time=end_time)
        
        for measurement in measurement_pb.measurements:
            self._weather_db.insert(measurement.time, measurement.air_temp, measurement.pressure, measurement.humidity, measurement.ground_temp, measurement.uv,
                                    measurement.uv_risk_lv, measurement.wind_speed, measurement.rainfall, measurement.rain_rate, measurement.wind_dir)
        
    def _get_time_ms(self):
        return int(time.time() * 1000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    