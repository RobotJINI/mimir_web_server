python3 -m grpc_tools.protoc -I=./protos/ --python_out=./model/ --grpc_python_out=./model/ ./protos/weather_measurement.proto

bokeh serve --show mimir_web_server
