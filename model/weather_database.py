import MySQLdb, datetime, http.client, json, os
import io
import time
import math
import logging
import threading
from utils.utils import get_time_ms
from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd


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
        
        self._historical_weather_count_template = 'SELECT COUNT(*) ' + \
                                                  'FROM weather_measurement ' + \
                                                  'WHERE time BETWEEN %s AND %s;'
                                                  
        self._historical_weather_template = 'SELECT time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir ' + \
                                            'FROM (' + \
                                            'SELECT time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir, ROW_NUMBER() OVER () AS row_num ' + \
                                            'FROM weather_measurement ' + \
                                            'WHERE time BETWEEN %s AND %s' + \
                                            ') subquery ' + \
                                            'WHERE MOD(row_num, %s) = 0;'

        self._current_weather_template = 'SELECT AVG(air_temp) as air_temp, AVG(pressure) as pressure, AVG(humidity) as humidity, ' + \
                                         'AVG(ground_temp) as ground_temp, AVG(uv) as uv, AVG(wind_speed) as wind_speed, MAX(wind_speed) as gust, ' + \
                                         'AVG(rainfall) as rainfall, AVG(rain_rate) as rain_rate ' + \
                                         'FROM weather_measurement ' + \
                                         'WHERE time BETWEEN %s AND %s;'

        self._latest_uv_template = 'SELECT uv_risk_lv FROM weather_measurement LIMIT 1;'

        self._current_wind_dir_template = 'SELECT wind_dir ' + \
                                          'FROM weather_measurement ' + \
                                          'WHERE time BETWEEN %s AND %s AND NOT wind_dir=-1;'
                                          
        self._select_bounds_template = 'SELECT %s FROM weather_measurement ORDER BY %s %s LIMIT 100;'
        
        self._approx_max_returns = 2000                                          
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
        
    def get_historical_weather(self, start_time=None, end_time=None, sub_sample=True):
        if end_time is None:
            end_time = get_time_ms()
        if start_time is None:
            start_time = end_time - 86400000 # 1 day ms
            
        count = self._get_historical_weather_count(start_time, end_time)
        modulus = 1
        if sub_sample:
            modulus = int(count / self._approx_max_returns) + 1
            
        params = (start_time, end_time, modulus)
        query_response = self._db.query(self._historical_weather_template % params)
        
        return self._query_to_cds(query_response)

    def get_current_weather(self, duration=120):
        end_time = get_time_ms()
        start_time = end_time - (duration * 1000)
        params = (start_time, end_time)
        return self._db.query(self._current_weather_template % params)

    def get_latest_uv_risk(self):
        query_response = self._db.query(self._latest_uv_template)
        logging.debug(f'get_latest_uv_risk: {query_response}')
        return query_response[0]['uv_risk_lv']

    def get_average_wind_dir(self, start_time, end_time):
        params = (start_time, end_time)
        query_response = self._db.query(self._current_wind_dir_template % params)
        return self._average_wind_dir(query_response)
    
    def get_upper_lower_bounds(self, field_name='pressure'):
        upper_bounds_resp = self._get_upper_bounds(field_name)
        lower_bounds_resp = self._get_lower_bounds(field_name)
        
        upper_bounds = [int(item[field_name]) for item in upper_bounds_resp]
        lower_bounds = [int(item[field_name]) for item in lower_bounds_resp]
        
        return upper_bounds, lower_bounds          
        
    def _get_upper_bounds(self, field_name):
        params = (field_name, field_name, 'DESC')
        return self._db.query(self._select_bounds_template % params)
        
    def _get_lower_bounds(self, field_name):
        params = (field_name, field_name, 'ASC')
        return self._db.query(self._select_bounds_template % params)

    def _get_historical_weather_count(self, start_time, end_time):
        params = (start_time, end_time)
        return (self._db.query(self._historical_weather_count_template % params))[0]['COUNT(*)']
    
    def _query_to_cds(self, query_response):
        measurement_dict = {
            'time': [int(db_measurement['time']) for db_measurement in query_response],
            'air_temp': [float(db_measurement['air_temp']) for db_measurement in query_response],
            'pressure': [float(db_measurement['pressure']) for db_measurement in query_response],
            'humidity': [float(db_measurement['humidity']) for db_measurement in query_response],
            'ground_temp': [float(db_measurement['ground_temp']) for db_measurement in query_response],
            'uv': [float(db_measurement['uv']) for db_measurement in query_response],
            'uv_risk_lv': [str(db_measurement['uv_risk_lv']) for db_measurement in query_response],
            'wind_speed': [float(db_measurement['wind_speed']) for db_measurement in query_response],
            'rainfall': [float(db_measurement['rainfall']) for db_measurement in query_response],
            'rain_rate': [float(db_measurement['rain_rate']) for db_measurement in query_response],
            'wind_dir': [float(db_measurement['wind_dir']) for db_measurement in query_response]
        }
        return ColumnDataSource(data=measurement_dict)
    
    def _average_wind_dir(self, query_response):
        sin_sum = 0.0
        cos_sum = 0.0

        flen = float(len(query_response))
        if flen == 0:
            return -1

        for angle_response in query_response:
            angle = angle_response['wind_dir']
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average
    
    def get_last_entry_time(self):
        return self._db.query(self._latest_time_template)[0]['time'] + 1
    