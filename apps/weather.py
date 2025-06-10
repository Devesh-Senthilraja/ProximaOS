from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import requests
from datetime import datetime

class Weather(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        search = QWidget(self)
        layout.addWidget(search, 1, 0, 1, 2)
        searchLayout = QGridLayout(search)
        searchLayout.setColumnStretch(1, 1)

        locationLabel = QLabel("Location:", self)
        locationLabel.setStyleSheet("font: bold 15px 'Arial';")
        searchLayout.addWidget(locationLabel, 0, 0)

        self.cityValue = QLineEdit(self)
        self.cityValue.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.cityValue.setFixedSize(900, 50)
        searchLayout.addWidget(self.cityValue, 0, 1)

        searchButton = QPushButton("Search", self)
        searchButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        searchButton.setFixedSize(100, 50)
        searchButton.clicked.connect(self.getWeather)
        searchLayout.addWidget(searchButton, 0, 2)

        weather = QWidget(self)
        weather.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        weather.setFixedSize(465, 620)
        layout.addWidget(weather, 2, 0)

        weatherLayout = QGridLayout(weather)
        self.temperatureLabel = QLabel("", self)
        self.temperatureLabel.setStyleSheet("font: bold 75px; color: black; border: 1px solid #f0f0f0;")
        weatherLayout.addWidget(self.temperatureLabel, 0, 0)

        weatherInfo = QWidget(self)
        weatherInfo.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        weatherInfo.setFixedSize(630, 620)
        layout.addWidget(weatherInfo, 2, 1)

        weatherInfoLayout = QGridLayout(weatherInfo)
        self.humidityLabel = QLabel("", self)
        self.humidityLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.pressureLabel = QLabel("", self)
        self.pressureLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.cloudsLabel = QLabel("", self)
        self.cloudsLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.sunriseLabel = QLabel("", self)
        self.sunriseLabel.setStyleSheet("border: 1px solid #f0f0f0;")
        self.sunsetLabel = QLabel("", self)
        self.sunsetLabel.setStyleSheet(" border: 1px solid #f0f0f0;")

        weatherInfoLayout.addWidget(self.humidityLabel, 0, 0)
        weatherInfoLayout.addWidget(self.pressureLabel, 1, 0)
        weatherInfoLayout.addWidget(self.cloudsLabel, 2, 0)
        weatherInfoLayout.addWidget(self.sunriseLabel, 3, 0)
        weatherInfoLayout.addWidget(self.sunsetLabel, 4, 0)

    def timeZone(self, utc_tz):
        local_time = datetime.utcfromtimestamp(utc_tz)
        return local_time.time()

    def getWeather(self):
        cityName = self.cityValue.text()
        weatherURL = 'http://api.openweathermap.org/data/2.5/weather?q=' + cityName + '&appid='
        try:
            weatherInfo = requests.get(weatherURL).json()

            if weatherInfo['cod'] == 200:
                kelvin = 273

                temp = int(weatherInfo['main']['temp'] - kelvin)
                pressure = weatherInfo['main']['pressure']
                humidity = weatherInfo['main']['humidity']
                sunrise = weatherInfo['sys']['sunrise']
                sunset = weatherInfo['sys']['sunset']
                timezone = weatherInfo['timezone']
                clouds = weatherInfo['clouds']['all']

                sunriseTime = self.timeZone(sunrise + timezone)
                sunsetTime = self.timeZone(sunset + timezone)

                self.temperatureLabel.setText(str(temp)+"°C")
                self.humidityLabel.setText("Humidity: "+str(humidity)+"%")
                self.pressureLabel.setText("Pressure: "+str(pressure)+" hPa")
                self.cloudsLabel.setText("Clouds: "+str(clouds)+"%")
                self.sunriseLabel.setText("Sunrise: "+str(sunriseTime))
                self.sunsetLabel.setText("Sunset: "+str(sunsetTime))

            else:
                self.temperatureLabel.setText("")
                self.humidityLabel.setText("")
                self.pressureLabel.setText("")
                self.cloudsLabel.setText("")
                self.sunriseLabel.setText("")
                self.sunsetLabel.setText("")
                QMessageBox.critical(self, cityName + " not found", "Please enter a valid city name.")
        except Exception:
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")