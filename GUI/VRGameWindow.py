from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VRGameWindow(object):
    def __init__(self,userId,sessionId,sessionTime):
        self.userId = userId
        self.sessionId = sessionId
        self.sessionTime = sessionTime
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 140, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.labelScore = QtWidgets.QLabel(self.centralwidget)
        self.labelScore.setGeometry(QtCore.QRect(110, 180, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelScore.setFont(font)
        self.labelScore.setObjectName("labelScore")

        self.labelScoreOutput = QtWidgets.QLabel(self.centralwidget)
        self.labelScoreOutput.setGeometry(QtCore.QRect(220, 180, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelScoreOutput.setFont(font)
        self.labelScoreOutput.setObjectName("labelScoreOutput")

        self.comboBoxSessionVRGame = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSessionVRGame.setGeometry(QtCore.QRect(200, 140, 91, 21))
        self.comboBoxSessionVRGame.setEditable(False)
        self.comboBoxSessionVRGame.setCurrentText("Select Session")
        self.comboBoxSessionVRGame.addItem("1/2")
        self.comboBoxSessionVRGame.addItem("2/2")
        self.comboBoxSessionVRGame.setMaxVisibleItems(16)
        self.comboBoxSessionVRGame.setObjectName("comboBoxSessionVRGame")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(210, 250, 151, 71))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.startFunction)

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(410, 250, 151, 71))
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stopFunction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VR Game"))
        self.label.setText(_translate("MainWindow", "Block"))
        self.labelScore.setText(_translate("MainWindow", "Score"))
        self.labelScoreOutput.setText(_translate("MainWindow", "Output"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

    def startFunction(self):
        print("Start Function")
        pass
    
    def stopFunction(self):
        print("Stop Function")
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_VRGameWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
