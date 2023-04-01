import time
import logging

from bokeh.io import curdoc
from bokeh.util.logconfig import basicConfig

from controller.controllers import DisplayController
from bokeh.embed import file_html
from bokeh.resources import CDN


class MimirWebServer:
    def __init__(self):
        self._build_ui()
        self.update()
        
    def _start_db_sync(self):
        self._db_sync_thread = threading.Thread(target=self._db_sync.run)
        self._db_sync_thread.start()
        
    def _build_ui(self): 
        self._display_controller = DisplayController()

        layout = self._display_controller.view()
        curdoc().add_root(layout)
        curdoc().add_periodic_callback(self.update, 5000)
        
        # Generate the HTML code for the Bokeh application with the CDN resources included
        html = file_html(layout, CDN, "Mimir Weather Station")
        curdoc().html = html

    def update(self):
         self._display_controller.update()


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
basicConfig()
mimir_web_server = MimirWebServer()
