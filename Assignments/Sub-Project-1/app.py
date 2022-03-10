
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

        self.no_data = QLabel("")
        self.no_data.setAlignment(QtCore.Qt.AlignCenter)

        #setting the headline of the app
        headline = QLabel('Check the weather of a place here')
        headline.setStyleSheet("color:white; font-weight: bold; font-size: 20px; text-align: center") #style for the headline
        headline.setContentsMargins(20, 10, 20, 0)
        headline.setAlignment(QtCore.Qt.AlignCenter)

        #input box for the city
        self.placeName = QLineEdit()
        self.placeName.setPlaceholderText("Enter the name of the place") #place holder for the input box
        self.placeName.setContentsMargins(20,5,20,5)
        self.placeName.setStyleSheet('font-size:15px; height: 40px;') #style for the input

        #creating the search button
        searchBtn = QPushButton('Search')
        searchBtn.setStyleSheet("background: #337ab7; color: white; font-weight: bold; border-radius: 6px; width: 100px; height: 35px;")
        searchBtn.clicked.connect(self.getData)

        #creating the layouts for the app
        inputLayout = QHBoxLayout()
        self.outerLayout = QVBoxLayout()
        topLayout = QFormLayout()
        bottomLayout = QVBoxLayout()

        #adding the widgets into the layouts
        inputLayout.addWidget(self.placeName)
        inputLayout.addWidget(searchBtn)
        topLayout.addRow(headline)
        topLayout.addRow(inputLayout)

        #styles and labels for the result
        styles = "color: white; font-weight:bold; font-size:18px;"
        self.weather = QLabel()
        self.temp_fahrenheit = QLabel()
        self.temp_celsius = QLabel()
        self.wind_speed = QLabel()
        self.humidity = QLabel() 
        self.image = QLabel()

        #timer for the next update
        self.count = 0
        self.start = False
        self.timer_label = QLabel(self)
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        timer = QtCore.QTimer(self) #creating a timer object
        timer.timeout.connect(self.showTime) #adding action to timer
        timer.start(100)
        
        #setting the styles for the result widgets
        self.weather.setAlignment(QtCore.Qt.AlignCenter)
        self.weather.setStyleSheet(styles)
        self.temp_fahrenheit.setStyleSheet(styles)
        self.temp_celsius.setStyleSheet(styles)
        self.wind_speed.setStyleSheet(styles)
        self.humidity.setStyleSheet(styles)
        self.timer_label.setStyleSheet(styles)
        self.no_data.setStyleSheet(styles)

        #layout for the results
        bottomLayoutTop = QHBoxLayout()
        bottomLayoutTop.addWidget(self.weather)
        bottomLayoutTop.addWidget(self.image)
        
        bottomLayoutMiddle = QHBoxLayout()
        bottomLayoutMiddle.addWidget(self.temp_celsius)
        bottomLayoutMiddle.addWidget(self.temp_fahrenheit)

        bottomLayoutBottom = QHBoxLayout()
        bottomLayoutBottom.addWidget(self.wind_speed)
        bottomLayoutBottom.addWidget(self.humidity)
        
        #adding all the layouts together
        bottomLayout.addLayout(bottomLayoutTop)
        bottomLayout.addLayout(bottomLayoutMiddle)
        bottomLayout.addLayout(bottomLayoutBottom)

        topLayout.addRow(bottomLayout)
        self.outerLayout.addLayout(topLayout)
        self.outerLayout.addWidget(self.no_data)
        self.outerLayout.addWidget(self.timer_label)

        #adding all the layouts to the out most layout
        self.setLayout(self.outerLayout)
        
        # setting  the size of window
        self.setFixedSize(700, 500)

    def showTime(self):
        if self.start:
            #decreasing the counter value
            self.count -= 1
            #checking if the timer is done and calling the function to call the api again
            if self.count == 0: 
                self.start = False
                self.getData()
  
        if self.start:
            #setting text for the counter label
            text = str(self.count / 10) + " s"
            self.timer_label.setText(text)

    def resetTimer(self):
        self.start = False
        #setting the counter to 1800s (1800s = 30m)
        self.count = 18000
        self.timer_label.setText("")
    
    def startTimer(self):
        self.start = True
        if self.count == 0:
            self.start = False

    def getData(self):
        #getting the value from the text box
        city = self.placeName.text()
        self.doRequest(city)

    def doRequest(self, city):  
        #creating the usl for api call 
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=703d74f2eac3edcf47136e9d91a0768d&units=imperial"
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)  
        
    #method for clearing all the data
    def clearData(self):
        self.no_data.setText("No data found")
        self.weather.setText("")
        self.temp_celsius.setText("")
        self.temp_fahrenheit.setText("")
        self.humidity.setText("")
        self.wind_speed.setText("")
        self.image.setPixmap(QPixmap(""))
        self.timer_label.setText("")

    def handleResponse(self, reply):
        er = reply.error()
        #if there's no error
        if er == QtNetwork.QNetworkReply.NoError:
            self.no_data.setText("")
            bytes_string = reply.readAll()
            data_dictionary = json.loads(str(bytes_string, "utf-8"))
            self.process_data(data_dictionary)

            self.count = 18000
            # setting text to the label
            self.timer_label.setText(str(self.count))
            self.startTimer()
        else:
            self.clearData()
            self.resetTimer()
            print("Error occured: ", er)
            print(reply.errorString())

    def process_data(self, data):
        #assigning all the data to their corresponding variable
        temp_fahrenheit = data["main"]["temp"]
        temp_degree = round(((temp_fahrenheit - 32) * 0.5556), 2)
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["main"]
        
        #getting the icon for the weather
        icon_url = 'http://openweathermap.org/img/wn/'+data["weather"][0]["icon"]+'@2x.png'
        icon = urllib.request.urlopen(icon_url).read()
        image = QImage()
        image.loadFromData(icon)
        
        #setting the text for all the labels for the results
        self.weather.setText("Weather: " + weather)
        self.temp_celsius.setText("Temperature (Fahrenheit): " + str(temp_fahrenheit) + "F")
        self.temp_fahrenheit.setText("Temperature (Celsius): " + str(temp_degree) + "\N{DEGREE SIGN}C")
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