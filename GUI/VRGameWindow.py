import os
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_VRGameWindow(object):
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
        
        self.labelVRGame = QtWidgets.QLabel(self.centralwidget)
        self.labelVRGame.setGeometry(QtCore.QRect(110, 70, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelVRGame.setFont(font)
        self.labelVRGame.setObjectName("labelVRGame")

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

        self.comboBoxSessionVRGame = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSessionVRGame.setGeometry(QtCore.QRect(200, 140, 91, 21))
        self.comboBoxSessionVRGame.setEditable(False)
        self.comboBoxSessionVRGame.setCurrentText("Select Session")
        self.comboBoxSessionVRGame.addItem("1")
        self.comboBoxSessionVRGame.addItem("2")
        self.comboBoxSessionVRGame.setMaxVisibleItems(16)
        self.comboBoxSessionVRGame.setObjectName("comboBoxSessionVRGame")

        self.labelLevel = QtWidgets.QLabel(self.centralwidget)
        self.labelLevel.setGeometry(QtCore.QRect(110, 210, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelLevel.setFont(font)
        self.labelLevel.setObjectName("labelLevel")

        self.lineEditLevel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLevel.setGeometry(QtCore.QRect(220, 220, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditLevel.setFont(font)
        self.lineEditLevel.setObjectName("lineEditLevel")

        self.labelScore = QtWidgets.QLabel(self.centralwidget)
        self.labelScore.setGeometry(QtCore.QRect(110, 270, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelScore.setFont(font)
        self.labelScore.setObjectName("labelScore")

        self.labelGoodcuts = QtWidgets.QLabel(self.centralwidget)
        self.labelGoodcuts.setGeometry(QtCore.QRect(110, 330, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelGoodcuts.setFont(font)
        self.labelGoodcuts.setObjectName("labelGoodcuts")

        self.labelMaxCombo = QtWidgets.QLabel(self.centralwidget)
        self.labelMaxCombo.setGeometry(QtCore.QRect(110, 390, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelMaxCombo.setFont(font)
        self.labelMaxCombo.setObjectName("labelMaxCombo")

        self.labelRank = QtWidgets.QLabel(self.centralwidget)
        self.labelRank.setGeometry(QtCore.QRect(110, 440, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelRank.setFont(font)
        self.labelRank.setObjectName("labelRank")

        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitButton.setGeometry(QtCore.QRect(150, 500, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")
        self.submitButton.clicked.connect(self.submitFunction)

        self.lineEditScore = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditScore.setGeometry(QtCore.QRect(220, 280, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditScore.setFont(font)
        self.lineEditScore.setObjectName("lineEditScore")
        
        self.lineEditGoodcuts = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditGoodcuts.setGeometry(QtCore.QRect(220, 340, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditGoodcuts.setFont(font)
        self.lineEditGoodcuts.setObjectName("lineEditGoodcuts")
        
        self.lineEditMaxCombo = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMaxCombo.setGeometry(QtCore.QRect(220, 390, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditMaxCombo.setFont(font)
        self.lineEditMaxCombo.setObjectName("lineEditMaxCombo")
        self.lineEditRank = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditRank.setGeometry(QtCore.QRect(220, 450, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditRank.setFont(font)
        self.lineEditRank.setObjectName("lineEditRank")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VR Game"))
        self.label.setText(_translate("MainWindow", "Block"))
        self.labelLevel.setText(_translate("MainWindow", "Level"))
        self.labelScore.setText(_translate("MainWindow", "Score"))
        self.labelGoodcuts.setText(_translate("MainWindow", "Goodcuts"))
        self.labelMaxCombo.setText(_translate("MainWindow", "Max Combo"))
        self.labelRank.setText(_translate("MainWindow", "Rank"))
        self.submitButton.setText(_translate("MainWindow", "Submit"))

    def submitFunction(self):
        fileName = os.path.join(self.PATH,f'output_block_{self.comboBoxSessionVRGame.currentText()}.txt')
        file = open(fileName,'w')
        text = self.labelLevel.text() + ' ' + self.lineEditLevel.text() + '\n' + self.labelScore.text() + ' ' + self.lineEditScore.text() + '\n' + self.labelGoodcuts.text() + ' ' + self.lineEditGoodcuts.text() + '\n' + self.labelMaxCombo.text() + ' ' + self.lineEditMaxCombo.text() + '\n' + self.labelRank.text() + ' ' + self.lineEditRank.text()
        file.write(text)
        file.close()
        self.lineEditLevel.clear()
        self.lineEditScore.clear()
        self.lineEditGoodcuts.clear()
        self.lineEditMaxCombo.clear()
        self.lineEditRank.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_VRGameWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
