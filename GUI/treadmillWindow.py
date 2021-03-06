from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import cv2
import os

import config
from sensor import SensorsHandler


class Ui_treadmillUI(object):
    def __init__(self,userId,sessionId,sessionTime):
        self.userId = userId
        self.sessionId = sessionId
        self.sessionTime = sessionTime
        self.PATH = None
        
    
    def setupUi(self, treadmillUi):
        self.centralwidget = QtWidgets.QWidget(treadmillUi)
        treadmillUi.setObjectName("treadmillUi")
        treadmillUi.resize(800, 600)
        self.cam_view = QtWidgets.QLabel(treadmillUi)
        self.cam_view.setGeometry(QtCore.QRect(200, 10, 400, 400))
        self.cam_view.setScaledContents(True)
        self.cam_view.setObjectName("cam_view")

        self.connect_btn = QtWidgets.QPushButton(treadmillUi)
        self.connect_btn.setGeometry(QtCore.QRect(60, 460, 160, 81))
        self.connect_btn.setAutoDefault(False)
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.clicked.connect(self.connect2Cam)

        self.record_btn = QtWidgets.QPushButton(treadmillUi)
        self.record_btn.setGeometry(QtCore.QRect(240, 460, 160, 81))
        self.record_btn.setAutoDefault(False)
        self.record_btn.setObjectName("record_btn")
        self.record_btn.clicked.connect(self.record)
        
        self.stop_btn = QtWidgets.QPushButton(treadmillUi)
        self.stop_btn.setGeometry(QtCore.QRect(420, 460, 160, 81))
        self.stop_btn.setAutoDefault(False)
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stopRecording)
        
        self.reset_btn = QtWidgets.QPushButton(treadmillUi)
        self.reset_btn.setGeometry(QtCore.QRect(600, 460, 160, 81))
        self.reset_btn.setAutoDefault(False)
        self.reset_btn.setObjectName("reset_btn")

        treadmillUi.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(treadmillUi)
        self.statusbar.setObjectName("statusbar")
        treadmillUi.setStatusBar(self.statusbar)

        self.retranslateUi(treadmillUi)
        QtCore.QMetaObject.connectSlotsByName(treadmillUi)

    def retranslateUi(self, treadmillUi):
        _translate = QtCore.QCoreApplication.translate
        treadmillUi.setWindowTitle(_translate("treadmillUi", "Treadmill Task"))
        self.connect_btn.setText(_translate("treadmillUi", "Connect Camera"))
        self.record_btn.setText(_translate("treadmillUi", "Start Recording"))
        self.stop_btn.setText(_translate("treadmillUi", "Stop Recording"))
        self.reset_btn.setText(_translate("treadmillUi", "Reset"))

    def ImageUpdateSlot(self,Image):
        self.cam_view.setPixmap(QPixmap.fromImage(Image))

    def connect2Cam(self):
        self.connect_btn.setEnabled(False)
        self.Worker1 = cameraThread(self.PATH)
        self.Worker1.start()
        
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.sesnsor = SensorsHandler(self.PATH,self.userId,self.sessionId)
        self.sesnsor.start()

    def record(self):
        
        self.record_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.connect_btn.setEnabled(False)

        self.record_btn.setStyleSheet("background-color:green")
        self.Worker1.record = True
        self.sesnsor.start_recording()
 

    def stopRecording(self):
        
        self.record_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.connect_btn.setEnabled(True)

        self.record_btn.setStyleSheet("background-color:light gray")
        self.Worker1.stop()
        self.sesnsor.close_sensor()

    def reset(self):
        pass

class cameraThread(QtCore.QThread):
    ImageUpdate = QtCore.pyqtSignal(QImage)

    def __init__(self,PATH,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.PATH = PATH
    
    def run(self):    
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(0)
        self.record = False
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        videoWriter = cv2.VideoWriter(os.path.join(self.PATH,'fCamFeed.mp4'), fourcc, 30.0, (int(self.Capture.get(3)),int(self.Capture.get(4))))
        
        while self.ThreadActive:
            ret, frame = self.Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.record:
                    videoWriter.write(frame)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        self.Capture.release()
        videoWriter.release()
        
        

    
    def stop(self):
        self.ThreadActive = False

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    treadmillUi = QtWidgets.QDialog()
    ui = Ui_treadmillUI()
    ui.setupUi(treadmillUi)
    treadmillUi.show()
    sys.exit(app.exec_())
