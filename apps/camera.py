from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import os
import random

class Camera(QWidget):
    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1080)
        self.cap.set(4, 720)
        self.existingIDs = []

        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)

        self.photoViewer = QLabel(self)
        self.photoViewer.setFixedSize(1105, 635)
        self.photoViewer.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        grid.addWidget(self.photoViewer, 0, 0, 1, 3)

        captureButton = QPushButton("Capture", self)
        captureButton.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        captureButton.setFixedSize(100, 50)
        captureButton.clicked.connect(self.capture)
        grid.addWidget(captureButton, 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFrames)
        self.timer.start(20)

    def checkID(self):
        if not os.path.exists("Photos"):
            os.mkdir("Photos")
        for x in os.listdir("Photos"):
            if x.endswith(".jpg"):
                id = x.replace("picture", "").replace(".png", "")
                self.existingIDs.append(id)

    def capture(self):
        self.checkID()
        ret, frame = self.cap.read()
        id = str(random.randint(1, 1000))
        while id in self.existingIDs:
            id = str(random.randint(1, 1000))
        if ret:
            outpath = os.path.join("Photos", f"picture{id}.png")
            cv2.imwrite(outpath, frame)
            cv2.waitKey(0)

    def showFrames(self):
        ret, frame = self.cap.read()
        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.photoViewer.width(), self.photoViewer.height(), Qt.KeepAspectRatio)
            self.photoViewer.setPixmap(QPixmap.fromImage(p))