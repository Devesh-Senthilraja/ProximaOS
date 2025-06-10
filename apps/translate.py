from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import googletrans
from textblob import TextBlob

class Translate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.languages = googletrans.LANGUAGES
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()

        languageSelectorLayout = QGridLayout()
        languageLabel = QLabel("Languages:")
        languageLabel.setStyleSheet("font: bold 15px 'Arial';")

        self.language1_ = QLineEdit()
        self.language1_.setFixedSize(430, 50)
        self.language1_.setText('English')
        self.language1_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        self.language2_ = QLineEdit()
        self.language2_.setFixedSize(430, 50)
        self.language2_.setText('English')
        self.language2_.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        translateButton = QPushButton("Translate")
        translateButton.setFixedSize(100, 50)
        translateButton.setStyleSheet("background-color: #d9d9d9; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        translateButton.clicked.connect(self.translate)

        languageSelectorLayout.addWidget(languageLabel, 0, 0)
        languageSelectorLayout.addWidget(self.language1_, 0, 1)
        languageSelectorLayout.addWidget(self.language2_, 0, 2)
        languageSelectorLayout.addWidget(translateButton, 0, 3)

        translateWindowLayout = QGridLayout()
        self.original = QTextEdit()
        self.original.setFixedSize(530, 645)
        self.original.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.translated = QTextEdit()
        self.translated.setFixedSize(530, 645)
        self.translated.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        translateWindowLayout.addWidget(self.original, 0, 0)
        translateWindowLayout.addWidget(self.translated, 0, 1)

        mainLayout.addLayout(languageSelectorLayout, 0, 0)
        mainLayout.addLayout(translateWindowLayout, 1, 0)
        self.setLayout(mainLayout)

    def translate(self):
        self.translated.clear()

        try:
            language1 = self.language1_.text().strip().lower()
            language2 = self.language2_.text().strip().lower()
            original_text = self.original.toPlainText().strip()
            words = TextBlob(original_text)

            if language1 != language2:
                language1key = next(key for key, value in self.languages.items() if value.lower() == language1)
                language2key = next(key for key, value in self.languages.items() if value.lower() == language2)
                words = words.translate(from_lang=language1key, to=language2key)

            self.translated.setPlainText(str(words))

        except StopIteration:
            QMessageBox.critical(self, 'Error', 'Invalid language code')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))