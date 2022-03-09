
# importing the required libraries
from PyQt5 import (
    QtCore,
    QtNetwork
)

import json
import urllib.request

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QWidget
)
from PyQt5.QtGui import (
    QImage,
    QPalette,
    QLinearGradient,
    QColor,
    QBrush,
    QPixmap
)
import sys
  
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
  
        # setting the background color of the main window
        p = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(0,0,0))
        gradient.setColorAt(1.0, QColor(44, 62, 80))
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

        # setting the title of the window
        self.setWindowTitle("Weather App")

        title = QLabel('Check the weather of a place here')
        title.setStyleSheet("color:white; font-weight: bold; font-size: 20px; text-align: center")
        title.setContentsMargins(20, 10, 20, 0)
        title.setAlignment(QtCore.Qt.AlignCenter)

        self.placeName = QLineEdit()
        self.placeName.setPlaceholderText("Enter the name of the place")
        self.placeName.setContentsMargins(20,5,20,5)
        self.placeName.setStyleSheet('font-size:15px; height: 40px;')

        searchBtn = QPushButton('Search')
        searchBtn.setStyleSheet("background: #337ab7; color: white; font-weight: bold; border-radius: 6px; width: 100px; height: 35px;")
        searchBtn.clicked.connect(self.get_data)

        inputLayout = QHBoxLayout()
        self.outerLayout = QVBoxLayout()
        topLayout = QFormLayout()
        bottomLayout = QVBoxLayout()

        inputLayout.addWidget(self.placeName)
        inputLayout.addWidget(searchBtn)
        topLayout.addRow(title)
        topLayout.addRow(inputLayout)

        styles = "color: white; font-weight:bold; font-size:18px;"
        self.weather = QLabel()
        self.temp_fahrenheit = QLabel()
        self.temp_celsius = QLabel()
        self.wind_speed = QLabel()
        self.humidity = QLabel() 
        self.image = QLabel()

        #for timer
        self.count = 0
        self.flag = False
        self.timer_label = QLabel(self)
        self.timer_label.setText("")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.weather.setAlignment(QtCore.Qt.AlignCenter)

        self.weather.setStyleSheet(styles)
        self.temp_fahrenheit.setStyleSheet(styles)
        self.temp_celsius.setStyleSheet(styles)
        self.wind_speed.setStyleSheet(styles)
        self.humidity.setStyleSheet(styles)
        self.timer_label.setStyleSheet(styles)

        bottomLayoutTop = QHBoxLayout()
        bottomLayoutTop.addWidget(self.weather)
        bottomLayoutTop.addWidget(self.image)
        
        bottomLayoutMiddle = QHBoxLayout()
        bottomLayoutMiddle.addWidget(self.temp_celsius)
        bottomLayoutMiddle.addWidget(self.temp_fahrenheit)

        bottomLayoutBottom = QHBoxLayout()
        bottomLayoutBottom.addWidget(self.wind_speed)
        bottomLayoutBottom.addWidget(self.humidity)
        

        bottomLayout.addLayout(bottomLayoutTop)
        bottomLayout.addLayout(bottomLayoutMiddle)
        bottomLayout.addLayout(bottomLayoutBottom)

        topLayout.addRow(bottomLayout)
        self.outerLayout.addLayout(topLayout)
        self.outerLayout.addWidget(self.timer_label)
        # self.outerLayout.addLayout(bottomLayout)

        self.setLayout(self.outerLayout)
        
        # setting  the size of window
        self.setFixedSize(700, 500)

    def showTime(self):
  
        # checking if flag is true
        if self.flag:
            self.count+= 1

        text = str(self.count / 10)
        self.timer_label.setText(text)

    def resetTimer(self):
        self.flag = False
        self.count = 0
        self.timer_label.setText("")
    
    def startTimer(self):
        self.flag = True

    def get_data(self):
        city = self.placeName.text()
        self.doRequest(city)

    def doRequest(self, city):   
        
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=703d74f2eac3edcf47136e9d91a0768d&units=imperial"
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)  
        
    def clearData(self):
        self.weather.setText("No data found")
        self.temp_celsius.setText("")
        self.temp_fahrenheit.setText("")
        self.humidity.setText("")
        self.wind_speed.setText("")
        self.image.setPixmap(QPixmap(""))
        self.timer_label.setText("")

    def handleResponse(self, reply):

        er = reply.error()
        
        if er == QtNetwork.QNetworkReply.NoError:
            bytes_string = reply.readAll()
            data_dictionary = json.loads(str(bytes_string, "utf-8"))
            self.process_data(data_dictionary)

            # creating a timer object
            timer = QtCore.QTimer(self)
            # adding action to timer
            timer.timeout.connect(self.showTime)
            # update the timer every tenth second
            timer.start(100)
            self.startTimer()
        else:
            self.clearData()
            self.resetTimer()
            print("Error occured: ", er)
            print(reply.errorString())

    def process_data(self, data):
        temp_fahrenheit = data["main"]["temp"]
        temp_degree = round(((temp_fahrenheit - 32) * 0.5556), 2)
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["main"]
        
        icon_url = 'http://openweathermap.org/img/wn/'+data["weather"][0]["icon"]+'@2x.png'
        icon = urllib.request.urlopen(icon_url).read()
        image = QImage()
        image.loadFromData(icon)
        
        self.weather.setText("Weather: " + weather)
        self.temp_celsius.setText("Temperature (Fahrenheit): " + str(temp_fahrenheit))
        self.temp_fahrenheit.setText("Temperature (Celsius): " + str(temp_degree))
        self.humidity.setText("Wind Speed (miles/hour): " + str(wind_speed))
        self.wind_speed.setText("Humidity: " + str(humidity))
        pixmap = QPixmap(image)
        self.image.setPixmap(pixmap)
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = MainWindow()
window.show()
  
# start the app
sys.exit(App.exec_())