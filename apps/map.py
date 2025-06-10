from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from geopy.geocoders import Nominatim
import folium
import os

class Map(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)

        location_label = QLabel("Location:", self)
        location_label.setStyleSheet("font: bold 15px 'Arial';")

        self.address_input = QLineEdit(self)
        self.address_input.setFixedSize(900, 50)
        self.address_input.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.address_input.setFixedHeight(40)

        search_button = QPushButton("Search", self)
        search_button.setFixedSize(100, 50)
        search_button.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        search_button.clicked.connect(self.update_map)

        main_layout.addWidget(location_label, 0, 0, 1, 1)
        main_layout.addWidget(self.address_input, 0, 1, 1, 8)
        main_layout.addWidget(search_button, 0, 9, 1, 1)

        self.map_view = QWebEngineView(self)
        self.map_view.setFixedSize(1105, 645)
        self.map_view.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        main_layout.addWidget(self.map_view, 1, 0, 1, 10)

        self.update_map(initial=True)

    def update_map(self, initial=False):
        address = "Pleasanton, CA" if initial else self.address_input.text()
        self.create_map(address)

    def create_map(self, address):
        geolocator = Nominatim(user_agent="map_app")
        location = geolocator.geocode(address)

        if location:
            map_obj = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
            folium.Marker([location.latitude, location.longitude], tooltip=address).add_to(map_obj)
        else:
            map_obj = folium.Map(location=[0, 0], zoom_start=2)
            folium.Marker([0, 0], tooltip="Location not found").add_to(map_obj)

        map_file = os.path.join(os.path.dirname(__file__), "../resources/map.html")
        map_obj.save(map_file)
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(map_file)))