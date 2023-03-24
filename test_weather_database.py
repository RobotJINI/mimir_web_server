from model.server_db import WeatherDatabaseSync
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
wds = WeatherDatabaseSync()
wds.run()