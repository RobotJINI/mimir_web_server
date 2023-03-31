import time
import logging

from bokeh.io import curdoc
from bokeh.util.logconfig import basicConfig

from controller.controllers import DisplayController
import model.theme


class MimirWebServer:
    def __init__(self):
        self._theme = model.theme.DefaultTheme()
        self._build_ui()
        self.update()
        
    def _start_db_sync(self):
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def _build_ui(self): 
        self._display_controller = DisplayController()

        curdoc().add_root(self._display_controller.ui)

        curdoc().add_periodic_callback(self.update, 5000)
        curdoc().title = "Mimir Weather Station"

    def update(self):
         self._display_controller.update()


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
basicConfig()
mimir_web_server = MimirWebServer()
