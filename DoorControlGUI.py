import sys
import board
import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QApplication
import time
from functools import partial
from threading import Thread

Outer = 22
Inner = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(Outer, GPIO.OUT)
GPIO.setup(Inner, GPIO.OUT)
GPIO.output(Outer, GPIO.HIGH)
GPIO.output(Inner, GPIO.HIGH)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Timer = QtWidgets.QLCDNumber(self.centralwidget)
        self.Timer.setObjectName("Timer")
        self.horizontalLayout.addWidget(self.Timer)
        self.OuterSwitch = QtWidgets.QPushButton(self.centralwidget)
        self.OuterSwitch.setObjectName("OuterSwitch")
        self.horizontalLayout.addWidget(self.OuterSwitch)
        self.InnerSwitch = QtWidgets.QPushButton(self.centralwidget)
        self.InnerSwitch.setObjectName("InnerSwitch")
        self.horizontalLayout.addWidget(self.InnerSwitch)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.OuterSwitch.setText(_translate("MainWindow", "Open Outer Door"))
        self.InnerSwitch.setText(_translate("MainWindow", "Open Inner Door"))


class ControlMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.OuterSwitch.clicked.connect(self.OuterControl)
        self.ui.InnerSwitch.clicked.connect(self.InnerControl)

        self.current_timer = None
        self.LCD_timer = None
        self.i = 120

    def LCDtimer(self):
        if self.LCD_timer:
            self.LCD_timer.stop()
            self.LCD_timer.deleteLater()
        self.LCD_timer = QtCore.QTimer()
        self.LCD_timer.start(0)

        self.LCD_timer.timeout.connect(self.updateLCDNumber)

    def starttimer(self):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer.deleteLater()
        self.i = 120
        
        self.current_timer = QtCore.QTimer()
        self.current_timer.setSingleShot(True)
        self.current_timer.start(121000)
        self.current_timer.timeout.connect(self.InnerSwitchOn)

    def updateLCDNumber(self):
        if self.i != 0:
            QtTest.QTest.qWait(1000)
            self.i -= 1
            self.ui.Timer.display(self.i)

    def InnerSwitchOn(self):
        self.ui.InnerSwitch.setEnabled(True)

    def OuterControl(self):
        if GPIO.input(Inner) == 0:  # InnerDoorOpen
            return GPIO.output(Outer, GPIO.HIGH), print("Please Close Inner Door")
        elif GPIO.input(Outer) == 1:  # Outer Door Close
            self.ui.OuterSwitch.setText(QtWidgets.QApplication.translate("MainWindow", "Close Outer Door", None))
            QtWidgets.QApplication.processEvents()
            
            return GPIO.output(Outer, GPIO.LOW)  # Open Outer Door
        elif GPIO.input(Outer) == 0:  # OuterDoor Open
            self.ui.InnerSwitch.setEnabled(False)
            self.ui.OuterSwitch.setText(QtWidgets.QApplication.translate("MainWindow", "Open Outer Door", None))
            QtWidgets.QApplication.processEvents()
            self.ui.Timer.display(120)
            self.LCDtimer()
            self.starttimer()

            ##            if self.current_timer ==3000:
            ##                self.ui.InnerSwitch.setEnabled(True)
            ##            else:

            ##            QtCore.QTimer.singleShot(3000,partial(self.ui.InnerSwitch.setEnabled,True))
            return GPIO.output(Outer, GPIO.HIGH)  # Close OuterDoor

    def InnerControl(self):
        if GPIO.input(Outer) == 0:  # Outer Open
            return GPIO.output(Inner, GPIO.HIGH), print("Please Close Outer Door")
        elif GPIO.input(Inner) == 1:  # Inner Door Close
            self.ui.InnerSwitch.setText(QtWidgets.QApplication.translate("MainWindow", "Close Inner Door", None))
            QtWidgets.QApplication.processEvents()
            return GPIO.output(Inner, GPIO.LOW)  # Open Inner
        elif GPIO.input(Inner) == 0:
            self.ui.InnerSwitch.setText(QtWidgets.QApplication.translate("MainWindow", "Open Inner Door", None))
            QtWidgets.QApplication.processEvents()
            return GPIO.output(Inner, GPIO.HIGH)  # Close Inner





            # Troubleshoot-comment in

    sys.excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
    MainWindow.show()
    sys.exit(app.exec_())
