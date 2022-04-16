from PyQt5 import QtCore, QtGui, QtWidgets
from sensor import SensorsHandler
import sys
sys.path.insert(0,'/home/heracleia/Desktop/va-experiment-setup/')
from muse import MuseDataCollection
import threading
from signal import signal, SIGPIPE, SIG_DFL


class Ui_BaselineReadingWindow(object):
    def __init__(self,userId,sessionId,sessionTime):
        self.userId = userId
        self.sessionId = sessionId
        self.sessionTime = sessionTime
        self.PATH = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 80, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(110, 210, 161, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.connectButton.setFont(font)
        self.connectButton.setObjectName("connectButton")
        self.connectButton.clicked.connect(self.connectFunction)
        
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(320, 210, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.recordButton.setFont(font)
        self.recordButton.setObjectName("recordButton")
        self.recordButton.clicked.connect(self.recordFunction)
        
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(520, 210, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stopButton.setFont(font)
        self.stopButton.setObjectName("stopButton")
        self.stopButton.clicked.connect(self.stopFunction)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Baseline Reading"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.recordButton.setText(_translate("MainWindow", "Record"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

    def connectFunction(self):
        self.sensor = SensorsHandler(self.PATH,self.userId,self.sessionId)
        self.muse = MuseDataCollection.MuseDataCollection(self.PATH)
        self.sensor.start()

    def recordFunction(self):
        self.sensor.start_recording()
        self.raw_data_thread = threading.Thread(target=self.muse.recordData,args=())
        self.neuro_data_thread = threading.Thread(target=self.muse.collectNeuroData,args=())
        signal(SIGPIPE, SIG_DFL)
        self.raw_data_thread.start()
        self.neuro_data_thread.start()

    def stopFunction(self):
        self.sensor.close_sensor()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_BaselineReadingWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
