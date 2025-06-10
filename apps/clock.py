from PyQt5.QtWidgets import QWidget, QGridLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPen, QColor
import math

class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view, 0, 0, 1, 1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

        self.resize(650, 650)
        self.setWindowTitle('Clock')

    def updateClock(self):
        self.scene.clear()
        now = QTime.currentTime()
        hour, minute, second = now.hour() % 12, now.minute(), now.second()

        pen = QPen(QColor("#373433"))
        pen.setWidth(2)
        self.scene.addEllipse(2, 2, 600, 600, pen)

        for hour_ in range(12):
            angle = hour_ * math.pi / 6 - math.pi / 2
            x = 600 / 2 + 0.7 * 600 / 2 * math.cos(angle)
            y = 600 / 2 + 0.7 * 600 / 2 * math.sin(angle)
            text = str(12 if hour_ == 0 else hour_)
            self.scene.addText(text).setPos(x, y - 10)

        for minute_ in range(60):
            angle = minute_ * math.pi / 30 - math.pi / 2
            x1 = 600 / 2 + 0.8 * 600 / 2 * math.cos(angle)
            y1 = 600 / 2 + 0.8 * 600 / 2 * math.sin(angle)
            x2 = 600 / 2 + 0.9 * 600 / 2 * math.cos(angle)
            y2 = 600 / 2 + 0.9 * 600 / 2 * math.sin(angle)
            self.scene.addLine(x1, y1, x2, y2, pen)

        hourAngle = (hour + minute / 60) * math.pi / 6 - math.pi / 2
        hourX = 600 / 2 + 0.5 * 600 / 2 * math.cos(hourAngle)
        hourY = 600 / 2 + 0.5 * 600 / 2 * math.sin(hourAngle)
        self.scene.addLine(600 / 2, 600 / 2, hourX, hourY, pen)

        minuteAngle = (minute + second / 60) * math.pi / 30 - math.pi / 2
        minuteX = 600 / 2 + 0.7 * 600 / 2 * math.cos(minuteAngle)
        minuteY = 600 / 2 + 0.7 * 600 / 2 * math.sin(minuteAngle)
        self.scene.addLine(600 / 2, 600 / 2, minuteX, minuteY, pen)

        secondAngle = second * math.pi / 30 - math.pi / 2
        secondX = 600 / 2 + 0.6 * 600 / 2 * math.cos(secondAngle)
        secondY = 600 / 2 + 0.6 * 600 / 2 * math.sin(secondAngle)
        pen.setColor(QColor("red"))
        pen.setWidth(2)
        self.scene.addLine(600 / 2, 600 / 2, secondX, secondY, pen)