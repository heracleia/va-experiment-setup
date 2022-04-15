from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_2BackGameWindow(object):
    def __init__(self,userId,sessionId,sessionTime):
        self.userId = userId
        self.sessionId = sessionId
        self.sessionTime = sessionTime
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(110, 250, 151, 71))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.startFunction)

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(310, 250, 151, 71))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stopFunction)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(500, 250, 151, 71))
        self.resetButton.setObjectName("pushButton")
        self.resetButton.clicked.connect(self.resetFunction)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 140, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.labelSession = QtWidgets.QLabel(self.centralwidget)
        self.labelSession.setGeometry(QtCore.QRect(460, 140, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelSession.setFont(font)
        self.labelSession.setObjectName("labelSession")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "2 Back Game"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.label.setText(_translate("MainWindow", "2-Back Game:"))

    def startFunction(self):
        print("Start Function")
        pass
    
    def stopFunction(self):
        print("Stop Function")
        pass
    
    def resetFunction(self):
        print("Reset Function")
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_2BackGameWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
