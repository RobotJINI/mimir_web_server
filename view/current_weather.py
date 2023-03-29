from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, Paragraph
from bokeh.layouts import column


class CurrentWeather():
    def __init__(self):
        super().__init__()
        self._cur_weather = None

    def make_plot(self, dataframe):
        self._cur_weather = Paragraph(text=f'{dataframe}')
        return self._cur_weather

    def update_plot(self, dataframe):
        if self._cur_weather is not None:
            self._cur_weather.text = f'{dataframe}'
        else:
            print("Error current weather module not initialized.")
