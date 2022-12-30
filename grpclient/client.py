from __future__ import print_function

import logging

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import model.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc


class WeatherGrpcClient:
    def __init__(self, ip='192.168.1.248', port='50051'):
        self._ip = ip
        self._port = port
        self._channel = grpc.insecure_channel(f'{self._ip}:{self._port}')
        self._stub = weather_measurement_pb2_grpc.WeatherServerStub(self._channel)
        
    def get_update(self, start_time=None, end_time=None):
        if end_time is None:
            end_time = self._get_time_ms()
        if start_time is None:
            start_time = end_time - 10000
        
        response = self._stub.get_current_weather(weather_measurement_pb2.CurrentWeatherRequest(duration=int(120)))
        print(f'response:{response}')
        return response
    
    def _get_time_ms(self):
        return time.time() * 1000
