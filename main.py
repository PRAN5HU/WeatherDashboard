import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListWidget
from PyQt5.QtGui import QFont
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Weather App')
        self.resize(800, 600)  # Set initial size to fit the window

        # Create a layout
        layout = QVBoxLayout()

        # Heading
        heading_label = QLabel('Temperature')
        heading_label.setFont(QFont("Arial", 16, QFont.Bold))
        heading_label.setStyleSheet("color: #333333;")  # Set text color using CSS
        layout.addWidget(heading_label)

        # Create and add widgets to the layout
        self.city_label = QLabel('Enter city name:')
        self.city_label.setStyleSheet("color: #666666;")  # Set text color using CSS
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit(self)
        self.city_input.setStyleSheet("background-color: #f2f2f2; border: 1px solid #cccccc;")  # Set background color and border using CSS
        layout.addWidget(self.city_input)

        # Create buttons layout
        buttons_layout = QVBoxLayout()

        self.get_weather_button = QPushButton('Get Weather', self)
        self.get_weather_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px; cursor: pointer;")  # Set button style using CSS
        self.get_weather_button.clicked.connect(self.get_weather)
        buttons_layout.addWidget(self.get_weather_button)

        self.get_weather_pin_button = QPushButton('Get Weather and Pin', self)
        self.get_weather_pin_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px; cursor: pointer;")  # Set button style using CSS
        self.get_weather_pin_button.clicked.connect(self.get_weather_and_pin)
        buttons_layout.addWidget(self.get_weather_pin_button)

        self.refresh_button = QPushButton('Refresh Pinned Data', self)
        self.refresh_button.setStyleSheet("background-color: #008CBA; color: white; border: none; padding: 10px 24px; cursor: pointer;")  # Set button style using CSS
        self.refresh_button.clicked.connect(self.refresh_pinned_data)
        buttons_layout.addWidget(self.refresh_button)

        layout.addLayout(buttons_layout)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        # List to display pinned cities
        self.pinned_list = QListWidget()
        layout.addWidget(self.pinned_list)

        # Set the layout on the application's window
        self.setLayout(layout)

    def get_weather(self):
        city = self.city_input.text()
        self.display_weather(city)

    def get_weather_and_pin(self):
        city = self.city_input.text()
        weather_info = self.display_weather(city)
        if weather_info:
            self.pin_weather(city, weather_info)

    def display_weather(self, city):
        weather_api_key = "0244e99d6894ff1aa3d4dce05e0c80f6"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}"

        try:
            main_page = requests.get(url).json()
            if main_page.get("cod") != 200:
                self.result_label.setText(f"Error: {main_page.get('message')}")
            else:
                temp = main_page["main"]["temp"]
                feels_like = main_page["main"]["feels_like"]
                humidity = main_page["main"]["humidity"]
                visibility = main_page["visibility"]
                wind_speed = main_page["wind"]["speed"]
                weather1 = main_page["weather"][0]["main"]

                temperature = temp

                temperature_color = self.get_temperature_color(temperature)

                # Change text color of weather information
                weather_info = (
                    f"The weather in {city} is {weather1} with a temperature of {temperature}°C.\n"
                    f"Feels Like: {feels_like}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Visibility: {visibility / 1000} km\n"
                    f"Wind Speed: {wind_speed} m/s"
                )
                self.result_label.setText(weather_info)
                return weather_info
        except requests.exceptions.RequestException as e:
            self.result_label.setText("Error: Unable to fetch data")
            return None

    def pin_weather(self, city, weather_info):
        pinned_cities = [self.pinned_list.item(index).text().split(':')[0] for index in range(self.pinned_list.count())]
        if city not in pinned_cities:
            item = f"{city}: {weather_info}"
            self.pinned_list.addItem(item)
        else:
            self.result_label.setText("Error: This city is already pinned.")

    def refresh_pinned_data(self):
        for index in range(self.pinned_list.count()):
            item_text = self.pinned_list.item(index).text()
            city = item_text.split(':')[0]
            weather_info = self.display_weather(city)
            if weather_info:
                self.pinned_list.item(index).setText(f"{city}: {weather_info}")

    def get_temperature_color(self, temperature):
        if temperature < 5:
            return "blue"
        elif temperature >= 5 and temperature < 15:
            return "lightblue"
        elif temperature >= 15 and temperature < 25:
            return "green"
        elif temperature >= 25 and temperature < 30:
            return "orange"
        else:
            return "red"


def main():
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
