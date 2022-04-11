from PyQt5 import QtCore, QtGui, QtWidgets
import cv2



class Ui_gaitUI(object):
    def setupUi(self, gaitUI):
        gaitUI.setObjectName("gaitUI")
        gaitUI.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(gaitUI)
        self.fCam_view = QtWidgets.QLabel(gaitUI)
        self.fCam_view.setGeometry(QtCore.QRect(40, 10, 351, 341))
        self.fCam_view.setText("")
        self.fCam_view.setScaledContents(True)
        self.fCam_view.setObjectName("fCam_view")
        self.sCam_view = QtWidgets.QLabel(gaitUI)
        self.sCam_view.setGeometry(QtCore.QRect(429, 10, 361, 331))
        self.sCam_view.setScaledContents(True)
        self.sCam_view.setObjectName("sCam_view")
        
        self.connect_btn = QtWidgets.QPushButton(gaitUI)
        self.connect_btn.setGeometry(QtCore.QRect(60, 460, 160, 81))
        self.connect_btn.setAutoDefault(False)
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.clicked.connect(self.connect2Cam)

        self.record_btn = QtWidgets.QPushButton(gaitUI)
        self.record_btn.setGeometry(QtCore.QRect(240, 460, 160, 81))
        self.record_btn.setAutoDefault(False)
        self.record_btn.setObjectName("record_btn")
        self.record_btn.clicked.connect(self.record)

        self.stop_btn = QtWidgets.QPushButton(gaitUI)
        self.stop_btn.setGeometry(QtCore.QRect(420, 460, 160, 81))
        self.stop_btn.setAutoDefault(False)
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.clicked.connect(self.stop)

        self.reset_btn = QtWidgets.QPushButton(gaitUI)
        self.reset_btn.setGeometry(QtCore.QRect(600, 460, 160, 81))
        self.reset_btn.setAutoDefault(False)
        self.reset_btn.setObjectName("reset_btn")
        self.reset_btn.clicked.connect(self.reset)

        gaitUI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(gaitUI)
        self.statusbar.setObjectName("statusbar")
        gaitUI.setStatusBar(self.statusbar)

        self.labelSessionGait = QtWidgets.QLabel(self.centralwidget)
        self.labelSessionGait.setGeometry(QtCore.QRect(60, 400, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelSessionGait.setFont(font)
        self.labelSessionGait.setObjectName("labelSessionGait")

        self.comboBoxSessionGait = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSessionGait.setGeometry(QtCore.QRect(200, 400, 100, 51))
        self.comboBoxSessionGait.setEditable(False)
        self.comboBoxSessionGait.setCurrentText("Select Session")
        self.comboBoxSessionGait.addItem("1/2")
        self.comboBoxSessionGait.addItem("2/2")
        self.comboBoxSessionGait.setMaxVisibleItems(16)
        self.comboBoxSessionGait.setObjectName("comboBoxSessionGait")

        self.retranslateUi(gaitUI)
        QtCore.QMetaObject.connectSlotsByName(gaitUI)

    def retranslateUi(self, gaitUI):
        _translate = QtCore.QCoreApplication.translate
        gaitUI.setWindowTitle(_translate("gaitUI", "GAIT"))
        self.connect_btn.setText(_translate("gaitUI", "Connect Camera"))
        self.record_btn.setText(_translate("gaitUI", "Start Recording"))
        self.stop_btn.setText(_translate("gaitUI", "Stop Recording"))
        self.reset_btn.setText(_translate("gaitUI", "Reset"))
        self.labelSessionGait.setText(_translate("gaitUI", "Session"))

    def frontCamUpdateSlot(self,fCamFeed):
        self.fCam_view.setPixmap(QtGui.QPixmap.fromImage(fCamFeed))

    def sideCamUpdateSlot(self,sCamFeed):
        self.sCam_view.setPixmap(QtGui.QPixmap.fromImage(sCamFeed))
        

    def connect2Cam(self):
        self.frontCam = frontCamThread()
        self.sideCam = sideCamThread()

        self.frontCam.start()
        self.sideCam.start()

        self.frontCam.fCam.connect(self.frontCamUpdateSlot)
        self.sideCam.sCam.connect(self.sideCamUpdateSlot)

    def record(self):
        print("Record Function")
        pass

    def stop(self):
        print("Stop")
        pass

    def reset(self):
        pass

class frontCamThread(QtCore.QThread):
    fCam = QtCore.pyqtSignal(QtGui.QImage)
    
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.fCam.emit(Pic)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()

class sideCamThread(QtCore.QThread):
    sCam = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                FlippedImage = cv2.flip(frame, 1)
                ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.sCam.emit(Pic)
    
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gaitUI = QtWidgets.QDialog()
    ui = Ui_gaitUI()
    ui.setupUi(gaitUI)
    gaitUI.show()
    sys.exit(app.exec_())
