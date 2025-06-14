from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QTextBrowser, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests

class News(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.popups = []
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()

        categoryLayout = QGridLayout()
        categoryLayout.setSpacing(10)

        buttons = [
            ("General", "general"),
            ("Entertainment", "entertainment"),
            ("Business", "business"),
            ("Sports", "sports"),
            ("Technology", "technology"),
            ("Health", "health")
        ]

        for i, (text, category) in enumerate(buttons):
            button = QPushButton(text)
            button.setStyleSheet("background-color: #d9d9d9; font: bold 13px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
            button.setFixedSize(150, 50)
            button.clicked.connect(lambda _, cat=category: self.getNews(cat))
            categoryLayout.addWidget(button, 0, i+1)

        categoryLayout.setColumnStretch(0, 1)
        categoryLayout.setColumnStretch(len(buttons)+1, 1)

        newsLayout = QGridLayout()
        self.newsOutput = QTextBrowser()
        self.newsOutput.setFixedSize(1105, 645)
        self.newsOutput.setStyleSheet("background-color: #f0f0f0; font: bold 17px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.newsOutput.setOpenExternalLinks(False)
        self.newsOutput.anchorClicked.connect(self.openPopup)
        newsLayout.addWidget(self.newsOutput, 0, 0)

        mainLayout.addLayout(categoryLayout, 0, 0)
        mainLayout.addLayout(newsLayout, 1, 0)
        self.setLayout(mainLayout)

    def getNews(self, type):
        newsURL = f"http://newsapi.org/v2/top-headlines?country=us&category={type}&apiKey="
        self.newsOutput.clear()
        try:
            newsInfo = (requests.get(newsURL).json())['articles']
            if newsInfo:
                for i, article in enumerate(newsInfo):
                    headline = f"\\n • {article['title']}\\n"
                    url = article['url']
                    self.newsOutput.append(f'<a href="{url}">{headline}</a><br>')
            else:
                self.newsOutput.setText("Sorry. No news available.")
        except Exception:
            QMessageBox.critical(self, 'No Internet', "Unable to connect to the internet at the moment.")

    def openPopup(self, url):
        webview = QWebEngineView()
        webview.setWindowTitle('News Article')
        webview.load(url)
        webview.show()
        self.popups.append(webview)