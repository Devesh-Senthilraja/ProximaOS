from apps.calculator import Calculator
from apps.calendar import Calendar
from apps.clock import Clock
from apps.notepad import Notepad
from apps.paint import Paint
from apps.image_viewer import ImageViewer
from apps.video_player import VideoPlayer
from apps.audio_player import AudioPlayer
from apps.camera import Camera
from apps.terminal import Terminal
from apps.weather import Weather
from apps.translate import Translate
from apps.dictionary import Dictionary
from apps.news import News
from apps.browser import Browser
from apps.map import Map

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPoint
from PyQt5.QtGui import QColor, QPalette, QIcon
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('OS')
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('lightgrey'))
        self.setPalette(palette)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 0)

        left_center_widget = QWidget()
        left_center_widget.setFixedSize(300, 900)
        left_center_widget.setStyleSheet("background-color: lightgrey; border-radius: 25px;")
        left_center_layout = QGridLayout()
        left_center_widget.setLayout(left_center_layout)
        grid_layout.addWidget(left_center_widget, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)
        grid_layout.setContentsMargins(10, 0, 0, 0)

        self.initButtonElements()
        self.addButtons(left_center_layout)

        bottom_center_widget = QWidget()
        bottom_center_widget.setFixedSize(625, 100)
        bottom_center_widget.setStyleSheet("background-color: lightgrey; border-radius: 25px;")
        bottom_center_layout = QGridLayout()
        bottom_center_widget.setLayout(bottom_center_layout)
        grid_layout.addWidget(bottom_center_widget, 1, 0, Qt.AlignBottom | Qt.AlignHCenter)
        grid_layout.setContentsMargins(10, 0, 0, 10)

        for i in range(3):
            inner_widget = QWidget()
            inner_widget.setStyleSheet("background-color: black; border-radius: 25px;")
            bottom_center_layout.addWidget(inner_widget, 0, i, Qt.AlignCenter)

            if i == 1:
                inner_widget.setFixedSize(325, 75)
                self.line_edit = QLineEdit()
                self.line_edit.setPlaceholderText("Enter app name")
                self.line_edit.setFixedSize(240, 50)
                self.line_edit.setStyleSheet("background-color: white; border-radius: 12px; padding: 5px;")
                search_button = QPushButton()
                icon_ = os.path.join(os.path.dirname(__file__), "../icons/searchButton.png")
                icon = QIcon(icon_)
                search_button.setIcon(icon)
                search_button.setFixedSize(50, 50)
                search_button.seticonsize(search_button.size())
                search_button.setStyleSheet("background-color: black; border: none;")
                search_button.clicked.connect(self.searchAndRunApp)
                inner_layout = QGridLayout()
                inner_widget.setLayout(inner_layout)
                inner_layout.addWidget(self.line_edit, 0, 0, Qt.AlignLeft)
                inner_layout.addWidget(search_button, 0, 1, Qt.AlignRight)

            else:
                inner_widget.setFixedSize(125, 75)
                if i == 0:
                    self.time_label = QLabel()
                    self.time_label.setStyleSheet("color: white;")
                    self.time_label.setAlignment(Qt.AlignCenter)
                    self.date_label = QLabel()
                    self.date_label.setStyleSheet("color: white;")
                    self.date_label.setAlignment(Qt.AlignCenter)
                    inner_layout = QGridLayout()
                    inner_widget.setLayout(inner_layout)
                    inner_layout.addWidget(self.time_label, 0, 0, Qt.AlignCenter)
                    inner_layout.addWidget(self.date_label, 1, 0, Qt.AlignCenter)
                    timer = QTimer(self)
                    timer.timeout.connect(self.updateDateTime)
                    timer.start(1000)
                    self.updateDateTime()
                if i == 2:
                    shutdown_button = QPushButton()
                    icon_ = os.path.join(os.path.dirname(__file__), "../icons/powerButton.png")
                    icon = QIcon(icon_)
                    shutdown_button.setIcon(icon)
                    shutdown_button.setFixedSize(50, 50)
                    shutdown_button.seticonsize(shutdown_button.size())
                    shutdown_button.setStyleSheet("background-color: black; border: none;")
                    shutdown_button.clicked.connect(self.close)
                    inner_layout = QGridLayout()
                    inner_widget.setLayout(inner_layout)
                    inner_layout.addWidget(shutdown_button, 0, 0, Qt.AlignCenter)
        bottom_center_layout.setContentsMargins(10, 0, 10, 0)

    def updateDateTime(self):
        current_time = QDateTime.currentDateTime()
        self.time_label.setText(current_time.toString("hh:mm:ss"))
        self.date_label.setText(current_time.toString("yyyy-MM-dd"))

    def searchAndRunApp(self):
        search_text = self.line_edit.text().strip().lower()
        for key, value in self.buttonElements.items():
            if value["name"] == search_text:
                value["action"]()
                break

    def initButtonElements(self):
        self.buttonElements = {
            "calculator": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/calculator.png"),
                "name": "calculator",
                "action": lambda: self.runApp(470, 740, "Calculator", Calculator)
            },
            "calendar": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/calendar.png"),
                "name": "calendar",
                "action": lambda: self.runApp(1130, 780, "Calendar", Calendar)
            },
            "clock": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/clock.png"),
                "name": "clock",
                "action": lambda: self.runApp(650, 700, "Clock", Clock)
            },
            "notepad": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/notepad.png"),
                "name": "notepad",
                "action": lambda: self.runApp(735, 990, "Notepad", Notepad)
            },
            "paint": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/paint.png"),
                "name": "paint",
                "action": lambda: self.runApp(735, 990, "Paint", Paint)
            },
            "photos": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/photoViewer.png"),
                "name": "photos",
                "action": lambda: self.runApp(1130, 780, "Image Viewer", ImageViewer)
            },
            "music": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/musicPlayer.png"),
                "name": "audio",
                "action": lambda: self.runApp(650, 700, "Audio Player", AudioPlayer)
            },
            "videos": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/videoPlayer.png"),
                "name": "videos",
                "action": lambda: self.runApp(1130, 780, "Video Player", VideoPlayer)
            },
            "camera": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/camera.png"),
                "name": "camera",
                "action": lambda: self.runApp(1130, 780, "Camera", Camera)
            },
            "terminal": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/terminal.png"),
                "name": "terminal",
                "action": lambda: self.runApp(1130, 780, "Terminal", Terminal)
            },
            "weather": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/weather.png"),
                "name": "weather",
                "action": lambda: self.runApp(1130, 780, "Weather", Weather)
            },
            "news": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/news.png"),
                "name": "news",
                "action": lambda: self.runApp(1130, 780, "News", News)
            },
            "map": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/map.png"),
                "name": "map",
                "action": lambda: self.runApp(1130, 780, "Map", Map)
            },
            "translate": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/translate.png"),
                "name": "translator",
                "action": lambda: self.runApp(1130, 780, "Translate", Translate)
            },
            "dictionary": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/dictionary.png"),
                "name": "dictionary",
                "action": lambda: self.runApp(1130, 780, "Dictionary", Dictionary)
            },
            "chat": {
                "icon": os.path.join(os.path.dirname(__file__), "icons/chat.png"),
                "name": "browser",
                "action": lambda: self.runApp(1130, 780, "Browser", Browser)
            }
        }  # App button elements will be added later by dependency injection

    def addButtons(self, layout):
        row = 0
        col = 0
        for key, value in self.buttonElements.items():
            if not os.path.isfile(value["icon"]):
                print(f"Icon file not found: {value['icon']}")
                continue
            button = QPushButton()
            icon = QIcon(value["icon"])
            button.setIcon(icon)
            button.setFixedSize(75, 75)
            button.seticonsize(button.size())
            button.setStyleSheet("background-color: lightgrey; border: none;")
            button.clicked.connect(value["action"])
            layout.addWidget(button, row, col)
            row += 1
            if row > 7:
                row = 0
                col += 1

class Window(QWidget):
    def __init__(self, width, height, title, app_widget_class):
        super().__init__()
        self.width_ = width
        self.height_ = height
        self.title = title
        self.app_widget_class = app_widget_class
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.width_, self.height_)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        title_bar = QWidget(self)
        title_bar.setStyleSheet("background-color: gray; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        title_bar.setFixedHeight(50)
        app_space = QWidget(self)
        app_space.setStyleSheet("background-color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        self.app_widget_class(app_space)
        layout.addWidget(title_bar, 0, 0, 1, -1)
        layout.addWidget(app_space, 1, 0, 1, -1)
        title_layout = QGridLayout()
        title_bar.setLayout(title_layout)
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: white; font: 20px 'Bernoru'")
        title_layout.addWidget(title_label, 0, 0)
        close_button = QPushButton('X')
        close_button.setStyleSheet("background-color: red; color: white; border-radius: 10px;")
        close_button.setFixedSize(30, 30)
        title_layout.addWidget(close_button, 0, 1)
        title_layout.setColumnStretch(0, 1)
        title_layout.setColumnStretch(1, 0)
        close_button.clicked.connect(self.close)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.draggable = True
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.oldPos = None