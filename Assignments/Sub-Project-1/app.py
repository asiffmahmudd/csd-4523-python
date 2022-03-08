
# importing the required libraries
from PyQt5 import QtCore
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
    QPalette,
    QLinearGradient,
    QColor,
    QBrush
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

        label = QLabel('Check the weather of a place here')
        label.setStyleSheet("color:white; font-weight: bold; font-size: 20px; text-align: center")
        label.setContentsMargins(20, 10, 20, 0)
        label.setAlignment(QtCore.Qt.AlignCenter)

        placeName = QLineEdit()
        placeName.setPlaceholderText("Enter the name of the place")
        placeName.setContentsMargins(20,5,20,5)
        placeName.setStyleSheet('font-size:15px; height: 40px;')

        searchBtn = QPushButton('Search')
        searchBtn.setContentsMargins(20, 0, 20, 5)
        searchBtn.resize(50,100)
        searchBtn.setStyleSheet("background: #337ab7; color: white; font-weight: bold; border-radius: 6px; height: 35px;")

        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()

        topLayout.addRow(label)
        topLayout.addRow(placeName)
        topLayout.addRow(searchBtn)

        outerLayout.addLayout(topLayout)

        self.setLayout(outerLayout)
        
        # setting  the size of window
        self.setFixedSize(700, 500)
        print(self.children())

  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = MainWindow()
window.show()
  
# start the app
sys.exit(App.exec_())