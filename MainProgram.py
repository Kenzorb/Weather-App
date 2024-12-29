# https://home.openweathermap.org/api_keys
# We used openwearmap api to obtain current weather data

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

background_path = "C:/Users/Kenzo/OneDrive/Personal Projects/VSCODE_Projects/Projects/Weather_App/images/Weather_icon.png"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1200, 500, 800, 300)
        self.setWindowIcon(QIcon(background_path))
        self.setWindowTitle("Weather App")
        self.initUI()

    def initUI(self):
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.windspeed_label = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button) #automatically centered when setLayout()
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.windspeed_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.windspeed_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.windspeed_label.setObjectName("windspeed_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;       
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic; 
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            QLabel#windspeed_label{
                font-size: 75px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):

        api_key = "2a615841c6e989b661db70b23e0f8d20"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()     #Try does not catch HTTP errors. Therefore we have to use this function to pass it to the except block
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
                print(data)

        except requests.exceptions.HTTPError as http_error:   #HTTPError checks for error code between 400-500
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:    #Network problems or invalid urls
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.windspeed_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67

        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        windspeed_ms = data["wind"]["speed"]
        windspeed_kmh = windspeed_ms * 3.6

        direction = data["wind"]["deg"]

        self.temperature_label.setText(f"{temperature_c:.1f}°C / {temperature_f:.1f}°F")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.windspeed_label.setText(f"Wind: {windspeed_kmh:.1f}km/h, {direction:.0f}°")


    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

    @staticmethod
    def get_compass_object(windspeed, direction):
        pass


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
