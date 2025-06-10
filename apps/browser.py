from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout(self)
        topLayout = QGridLayout()
        bottomLayout = QGridLayout()

        self.webView = QWebEngineView()
        self.webView.setFixedSize(1105, 645)
        self.webView.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.webView.setUrl(QUrl("https://www.google.com"))

        backButton = QPushButton()
        backButton.setIcon(QIcon("Icons/arrow1.png"))
        backButton.setFixedHeight(50)
        backButton.clicked.connect(self.webView.back)

        forwardButton = QPushButton()
        forwardButton.setIcon(QIcon("Icons/arrow2.png"))
        forwardButton.setFixedHeight(50)
        forwardButton.clicked.connect(self.webView.forward)

        homeButton = QPushButton()
        homeButton.setIcon(QIcon("Icons/home.png"))
        homeButton.setFixedHeight(50)
        homeButton.clicked.connect(lambda: self.webView.setUrl(QUrl("https://www.google.com")))

        self.urlLineEdit = QLineEdit()
        self.urlLineEdit.setFixedSize(850, 50)
        self.urlLineEdit.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        goButton = QPushButton("Go")
        goButton.setFixedSize(100, 50)
        goButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        goButton.clicked.connect(self.navigate)

        topLayout.addWidget(backButton, 0, 0)
        topLayout.addWidget(forwardButton, 0, 1)
        topLayout.addWidget(homeButton, 0, 2)
        topLayout.addWidget(self.urlLineEdit, 0, 3)
        topLayout.addWidget(goButton, 0, 4)

        bottomLayout.addWidget(self.webView, 0, 0)

        mainLayout.addLayout(topLayout, 0, 0)
        mainLayout.addLayout(bottomLayout, 1, 0)

    def navigate(self):
        url = self.urlLineEdit.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.google.com/search?q=" + url
        self.webView.setUrl(QUrl(url))