from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Div
from bokeh.layouts import column


class CurrentWeather():
    def __init__(self):
        self._template = """
            <div class='widget-div'>
                <span class='widget-label'>Air Temperature:</span>
                <span class='widget-value'>{air_temp}&deg;F</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Pressure:</span>
                <span class='widget-value'>{pressure} mb</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Humidity:</span>
                <span class='widget-value'>{humidity}%</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Ground Temperature:</span>
                <span class='widget-value'>{ground_temp}&deg;F</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>UV:</span>
                <span class='widget-value'>{uv}</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Wind Speed:</span>
                <span class='widget-value'>{wind_speed} mph</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Gust:</span>
                <span class='widget-value'>{gust} mph</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Rainfall:</span>
                <span class='widget-value'>{rainfall} in</span>
            </div>
            <div class='widget-div'>
                <span class='widget-label'>Rain Rate:</span>
                <span class='widget-value'>{rain_rate} in/hr</span>
            </div>
        """
        self._create_view()

    def _create_view(self):
        default_data = {'air_temp': '48.64', 
                        'pressure': '1010.74', 
                        'humidity': '26.40', 
                        'ground_temp': '44.27', 
                        'uv': '237.7', 
                        'wind_speed': '1.64', 
                        'gust': '2.54', 
                        'rainfall': '0E-8', 
                        'rain_rate': '0E-8'}
        html = self._template.format(air_temp=48.64, pressure=1010.74, humidity=26.40, ground_temp=44.27,
                                     uv=237.7, wind_speed=1.64, gust=2.54, rainfall=0, rain_rate=0)
        self._cur_weather = Div(text=html)
        
    def get_view(self):
        return self._cur_weather

    def update(self, dataframe):
        self._cur_weather.text = self._template.format(air_temp=dataframe['air_temp'], pressure=dataframe['pressure'], humidity=dataframe['humidity'], 
                                                       ground_temp=dataframe['ground_temp'],uv=dataframe['uv'], wind_speed=dataframe['wind_speed'],
                                                       gust=dataframe['gust'], rainfall=dataframe['rainfall'], rain_rate=dataframe['rain_rate'])
