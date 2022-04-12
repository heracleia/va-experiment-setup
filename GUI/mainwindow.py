from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import widgets
from gaitWindow import Ui_gaitUI
from treadmillWindow import Ui_treadmillUI
from twoBackGameWindow import Ui_2BackGameWindow
from VRGameWindow import Ui_VRGameWindow
import os
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 500)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startTest = QtWidgets.QPushButton(self.centralwidget)
        self.startTest.setGeometry(QtCore.QRect(30, 350, 331, 61))
        self.startTest.setFlat(False)
        self.startTest.setObjectName("startTest")
        self.startTest.clicked.connect(self.start_test)
        self.userId_Label = QtWidgets.QLabel(self.centralwidget)
        self.userId_Label.setGeometry(QtCore.QRect(50, 110, 101, 31))
        self.userId_Label.setObjectName("userId_Label")
        self.userID_Input = QtWidgets.QLineEdit(self.centralwidget)
        self.userID_Input.setGeometry(QtCore.QRect(180, 110, 113, 21))
        self.userID_Input.setObjectName("userID_Input")
        self.session_label = QtWidgets.QLabel(self.centralwidget)
        self.session_label.setGeometry(QtCore.QRect(50, 180, 71, 21))
        self.session_label.setObjectName("session_label")
        self.session_Input = QtWidgets.QLineEdit(self.centralwidget)
        self.session_Input.setGeometry(QtCore.QRect(180, 180, 113, 21))
        self.session_Input.setObjectName("session_Input")
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(50, 260, 60, 16))
        self.time_label.setObjectName("time_label")
        self.time_radio2 = QtWidgets.QRadioButton(self.centralwidget)
        self.time_radio2.setGeometry(QtCore.QRect(280, 260, 100, 20))
        self.time_radio2.setObjectName("time_radio2")
        self.time_radio1 = QtWidgets.QRadioButton(self.centralwidget)
        self.time_radio1.setGeometry(QtCore.QRect(180, 260, 100, 20))
        self.time_radio1.setObjectName("time_radio1")
        self.time_radio1.setChecked(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VA Experimental Setup"))
        self.startTest.setText(_translate("MainWindow", "START TEST"))
        self.userId_Label.setText(_translate("MainWindow", "User ID#"))
        self.session_label.setText(_translate("MainWindow", "Session ID"))
        self.time_label.setText(_translate("MainWindow", "Time"))
        self.time_radio2.setText(_translate("MainWindow", "Evening"))
        self.time_radio1.setText(_translate("MainWindow", "Morning"))

    def start_test(self):
        if self.time_radio1.isChecked():
            radio1_value = "Morning"
        else:
            radio1_value = "Evening"
        userID = self.userID_Input.text()
        sessionID = self.session_Input.text()

        self.w = QtWidgets.QMainWindow()
        self.ui = Ui_IndexWindow(userID,sessionID,radio1_value)
        self.ui.setupUi(self.w)
        # self.ui.userId__Value_Label.setText(userID)
        # self.ui.sessionId__Value_Label.setText(sessionID)
        # self.ui.radio__Value_Label.setText(radio1_value)
        
        self.ui.statusbar.showMessage(f"User ID:{userID}\t\t\t\t\t Session ID:{sessionID}\t\t\t\t\t Time:{radio1_value}")
        widget.addWidget(self.w)
        widget.resize(800,600)
        widget.setCurrentWidget(self.w)

class Ui_IndexWindow(object):
    def __init__(self,userId,sessionId,sessionTime):
        self.userId = userId
        self.sessionId = sessionId
        self.sessionTime = sessionTime

    def setupUi(self, TwoBackButton):

        TwoBackButton.setObjectName("TwoBackButton")
        TwoBackButton.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(TwoBackButton)
        self.centralwidget.setObjectName("centralwidget")
        
        self.GAITButton = QtWidgets.QPushButton(self.centralwidget)
        self.GAITButton.setGeometry(QtCore.QRect(140, 120, 161, 81))
        self.GAITButton.setObjectName("GAITButton")
        self.GAITButton.clicked.connect(self.gaitWindowFunction)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 120, 161, 81))
        self.pushButton.setObjectName("TwoBackButton")
        self.pushButton.clicked.connect(self.twoBackGameWindowFunction)

        self.comboBoxSession = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSession.setGeometry(QtCore.QRect(550, 120, 91, 21))
        self.comboBoxSession.setEditable(False)
        self.comboBoxSession.setCurrentText("Select Session")
        self.comboBoxSession.addItem("1/2")
        self.comboBoxSession.addItem("2/2")
        self.comboBoxSession.setMaxVisibleItems(16)
        self.comboBoxSession.setObjectName("comboBoxSession")
        
        self.VRGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.VRGameButton.setGeometry(QtCore.QRect(140, 250, 161, 81))
        self.VRGameButton.setObjectName("VRGameButton")
        self.VRGameButton.clicked.connect(self.VRGameWindowFunction)
        
        self.TreadmillButton = QtWidgets.QPushButton(self.centralwidget)
        self.TreadmillButton.setGeometry(QtCore.QRect(380, 250, 161, 81))
        self.TreadmillButton.setObjectName("TreadMillButton")
        self.TreadmillButton.clicked.connect(self.treadmillWindowFunction)
        
        self.LogOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.LogOutButton.setGeometry(QtCore.QRect(260, 380, 161, 81))
        self.LogOutButton.setObjectName("LogOutButton")
        self.LogOutButton.clicked.connect(self.end_test)
        self.LogOutButton.clicked.connect(TwoBackButton.close)

        TwoBackButton.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(TwoBackButton)
        self.statusbar.setObjectName("statusbar")
        TwoBackButton.setStatusBar(self.statusbar)

        self.retranslateUi(TwoBackButton)
        QtCore.QMetaObject.connectSlotsByName(TwoBackButton)

    def retranslateUi(self, TwoBackButton):
        _translate = QtCore.QCoreApplication.translate
        TwoBackButton.setWindowTitle(_translate("TwoBackButton", "MainWindow"))
        self.GAITButton.setText(_translate("TwoBackButton", "GAIT"))
        self.pushButton.setText(_translate("TwoBackButton", "2-Back"))
        self.VRGameButton.setText(_translate("TwoBackButton", "VR Game"))
        self.TreadmillButton.setText(_translate("TwoBackButton", "Treadmill"))
        self.LogOutButton.setText(_translate("TwoBackButton", "Log Out"))

    def gaitWindowFunction(self):
        self.w = QtWidgets.QMainWindow()
        self.ui = Ui_gaitUI() 
        self.ui.setupUi(self.w)
        self.ui.statusbar.showMessage(f"User ID:{self.userId}\t\t\t\t\t Session ID:{self.sessionId}\t\t\t\t\t Time:{self.sessionTime}")
        self.w.show()

    def treadmillWindowFunction(self):
        self.w = QtWidgets.QMainWindow()
        self.ui = Ui_treadmillUI(self.userId,self.sessionId,self.sessionTime)
        exists = os.path.exists(self.ui.RGBPATH)
        print(self.ui.RGBPATH)
        if not exists:
            os.makedirs(self.ui.RGBPATH)
        self.ui.setupUi(self.w)
        self.ui.statusbar.showMessage(f"User ID:{self.userId}\t\t\t\t\t Session ID:{self.sessionId}\t\t\t\t\t Time:{self.sessionTime}")
        self.w.show()

    def twoBackGameWindowFunction(self):
        self.w = QtWidgets.QMainWindow()
        self.ui = Ui_2BackGameWindow()
        self.ui.setupUi(self.w)
        self.ui.statusbar.showMessage(f"User ID:{self.userId}\t\t\t\t\t Session ID:{self.sessionId}\t\t\t\t\t Time:{self.sessionTime}")
        self.ui.labelSession.setText(self.comboBoxSession.currentText())
        self.w.show()

    def VRGameWindowFunction(self):
        self.w = QtWidgets.QMainWindow()
        self.ui = Ui_VRGameWindow()
        self.ui.setupUi(self.w)
        self.ui.statusbar.showMessage(f"User ID:{self.userId}\t\t\t\t\t Session ID:{self.sessionId}\t\t\t\t\t Time:{self.sessionTime}")
        self.w.show()

    def end_test(self):
        widget.resize(400,500)
        widget.setCurrentWidget(MainWindow)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    widget = QtWidgets.QStackedWidget()
    widget.addWidget(MainWindow)
    widget.resize(400,500)
    widget.show()
    sys.exit(app.exec_())
