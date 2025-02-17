import sys

import requests
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.uic.Compiler.qtproxies import QtCore
from PyQt6.QtCore import Qt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_KEY = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


class MainWindow(QMainWindow):
    q_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('untitled.ui', self)

        self.map_zoom = 17
        self.map_ll = [30.302580, 59.991670]
        self.map_key = ''

        self.refresh_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            if self.map_zoom < 21:
                self.map_zoom += 1
            self.refresh_map()
        if event.key() == Qt.Key.Key_PageDown:
            if self.map_zoom > 0 :
                self.map_zoom -= 1
            self.refresh_map()

    def refresh_map(self):
        mar_params = {
            "ll": ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'apikey': API_KEY
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        response = session.get('http://static-maps.yandex.ru/v1', params=mar_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.q_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
