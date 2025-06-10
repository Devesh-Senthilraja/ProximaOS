from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
import json
from difflib import get_close_matches
import os

class Dictionary(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        words_path = os.path.join(os.path.dirname(__file__), "../resources/words.json")
        self.wordsData = json.load(open(words_path)) if os.path.exists(words_path) else {}
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()

        searchLayout = QGridLayout()
        searchLabel = QLabel("Word:")
        searchLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.word_ = QLineEdit()
        self.word_.setFixedSize(900, 50)
        self.word_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        findButton = QPushButton("Search")
        findButton.setFixedSize(100, 50)
        findButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        findButton.clicked.connect(lambda: self.wordMeaning(self.word_.text()))

        searchLayout.addWidget(searchLabel, 0, 0)
        searchLayout.addWidget(self.word_, 0, 1)
        searchLayout.addWidget(findButton, 0, 2)

        viewerLayout = QGridLayout()
        self.info = QTextEdit()
        self.info.setFixedSize(1105, 645)
        self.info.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.info.setReadOnly(True)
        viewerLayout.addWidget(self.info, 0, 0)

        mainLayout.addLayout(searchLayout, 0, 0)
        mainLayout.addLayout(viewerLayout, 1, 0)
        self.setLayout(mainLayout)

    def printWord(self, def__):
        def_ = def__.replace("', '", "\\n •  ")
        def_ = def_.replace("['", " •  ")
        def_ = def_.strip("']")
        self.info.append(def_)

    def wordMeaning(self, word):
        word = word.lower()
        self.info.clear()

        if word in self.wordsData:
            self.printWord(str(self.wordsData[word]))
        elif word.title() in self.wordsData:
            self.printWord(str(self.wordsData[word.title()]))
        elif word.upper() in self.wordsData:
            self.printWord(str(self.wordsData[word.upper()]))
        elif len(get_close_matches(word, self.wordsData.keys())) > 0:
            similarWord = get_close_matches(word, self.wordsData.keys())[0]
            ans = QMessageBox.question(self, 'Confirmation', f"Did you mean {similarWord} instead?",
                                       QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.wordMeaning(similarWord)
        else:
            QMessageBox.critical(self, 'Error', "This word does not exist")