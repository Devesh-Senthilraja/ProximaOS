from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSlider, QColorDialog
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class Paint(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(15)

        self.canvas = QWidget()
        self.canvas.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.canvas.setMinimumSize(710, 850)
        self.path = []
        self.penWidth = 1
        self.color = Qt.black
        self.eraserOn = False

        self.canvas.mousePressEvent = self.mousePressEvent
        self.canvas.mouseMoveEvent = self.mouseMoveEvent
        self.canvas.paintEvent = self.paintEvent

        self.layout.addWidget(self.canvas, 0, 0, 1, 4)

        buttonLayout = QGridLayout()
        self.layout.addLayout(buttonLayout, 1, 0, 1, 4)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        self.penButton = QPushButton("Pen")
        self.penButton.setStyleSheet(btn_style)
        self.penButton.setFixedSize(100, 50)
        self.penButton.clicked.connect(self.pen)
        buttonLayout.addWidget(self.penButton, 0, 0)

        self.eraserButton = QPushButton("Eraser")
        self.eraserButton.setStyleSheet(btn_style)
        self.eraserButton.setFixedSize(100, 50)
        self.eraserButton.clicked.connect(self.eraser)
        buttonLayout.addWidget(self.eraserButton, 0, 1)

        self.colorButton = QPushButton("Color")
        self.colorButton.setStyleSheet(btn_style)
        self.colorButton.setFixedSize(100, 50)
        self.colorButton.clicked.connect(self.chooseColor)
        buttonLayout.addWidget(self.colorButton, 0, 2)

        self.sizeSlider = QSlider(Qt.Horizontal)
        self.sizeSlider.setFixedSize(200, 50)
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(10)
        self.sizeSlider.valueChanged.connect(self.setPenSize)
        buttonLayout.addWidget(self.sizeSlider, 0, 3)

        self.activeButton = self.penButton

    def pen(self):
        self.activeButton = self.penButton
        self.eraserOn = False

    def eraser(self):
        self.activeButton = self.eraserButton
        self.eraserOn = True

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            if self.eraserOn:
                self.pen()
                self.eraserButton.setChecked(True)

    def setPenSize(self):
        self.penWidth = self.sizeSlider.value()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.path.append({'points': [event.pos()], 'color': self.color, 'penWidth': self.penWidth, 'eraser': self.eraserOn})

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.path[-1]['points'].append(event.pos())
            self.canvas.update()

    def paintEvent(self, event):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.Antialiasing)

        for line in self.path:
            pen = QPen()
            pen.setWidth(line['penWidth'])
            pen.setColor(QColor("#f0f0f0") if line['eraser'] else line['color'])
            painter.setPen(pen)

            points = line['points']
            for i in range(1, len(points)):
                painter.drawLine(points[i - 1], points[i])