from __future__ import print_function

import logging
import pandas as pd

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import model.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc
from bokeh.models import ColumnDataSource


class WeatherGrpcClient:
    def __init__(self, ip='192.168.10.102', port='50051'):
        self._ip = ip
        self._port = port
        self._channel = grpc.insecure_channel(f'{self._ip}:{self._port}')
        self._stub = weather_measurement_pb2_grpc.WeatherServerStub(self._channel)

    def get_current_weather(self):
        response = self._stub.get_current_weather(weather_measurement_pb2.CurrentWeatherRequest(duration=int(120)))
        return response

    def get_measurements(self, start_time=None, end_time=None):
        if end_time is None:
            end_time = self._get_time_ms()
        if start_time is None:
            start_time = end_time - 8640000 # 1 day ms
            #start_time = end_time - 604800000 # 1 week ms
        print(f'start_time={start_time}, end_time={end_time}')
        response = self._stub.get_measurements(weather_measurement_pb2.MeasurementRequest(start_time=start_time, end_time=end_time))
        return self._measurement_pb_to_df(response)

    def _measurement_pb_to_df(self, measurement_pb):
        time = []
        air_temp = []
        pressure = []
        humidity = []
        ground_temp = []
        uv = []
        uv_risk_lv = []
        wind_speed = []
        rainfall = []
        rain_rate = []
        wind_dir = []

        for measurement in measurement_pb.measurements:
            time.append(measurement.time/1000)
            air_temp.append(measurement.air_temp)
            pressure.append(measurement.pressure)
            humidity.append(measurement.humidity)
            ground_temp.append(measurement.ground_temp)
            uv.append(measurement.uv)
            uv_risk_lv.append(measurement.uv_risk_lv)
            wind_speed.append(measurement.wind_speed)
            rainfall.append(measurement.rainfall)
            rain_rate.append(measurement.rain_rate)
            wind_dir.append(measurement.wind_dir)

        print(f'lens {len(air_temp)}, {len(ground_temp)}')
        return ColumnDataSource(data=dict(
                                    time=pd.to_datetime(time[::10], unit='s', origin='unix'),
                                    air_temp=air_temp[::10],
                                    pressure=pressure[::10],
                                    humidity=humidity[::10],
                                    ground_temp=ground_temp[::10],
                                    uv=uv[::10],
                                    uv_risk_lv=uv_risk_lv[::10],
                                    wind_speed=wind_speed[::10],
                                    rainfall=rainfall[::10],
                                    rain_rate=rain_rate[::10],
                                    wind_dir=wind_dir[::10]
                              ))


    def _get_time_ms(self):
        return round(time.time() * 1000)
