from __future__ import print_function

import logging
import pandas as pd
import socket

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import model.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc
from bokeh.models import ColumnDataSource


class WeatherGrpcClient:
    def __init__(self, hostname='mimir.local', port='50051'):
        self._ip = self._resolve_hostname(hostname)
        self._port = port
        self._channel = grpc.insecure_channel(f'{self._ip}:{self._port}')
        self._stub = weather_measurement_pb2_grpc.WeatherServerStub(self._channel)

    def get_measurements(self, start_time, end_time):
        logging.debug(f'start_time={start_time}, end_time={end_time}')
        return self._stub.get_measurements(weather_measurement_pb2.MeasurementRequest(start_time=start_time, end_time=end_time))
        
    def _resolve_hostname(self, hostname):
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror:
            logging.error(f"Hostname '{hostname}' could not be resolved. Defaulting to '192.168.10.102'.")
            return '192.168.10.102'
