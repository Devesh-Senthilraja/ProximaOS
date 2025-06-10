from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QPushButton, QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

class Notepad(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)
        layout.setSpacing(15)

        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.textEdit.setFixedSize(710, 850)
        layout.addWidget(self.textEdit, 0, 0, 1, 4)

        buttonLayout = QGridLayout()
        layout.addLayout(buttonLayout, 1, 0, 1, 4)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"

        newButton = QPushButton('New')
        newButton.setStyleSheet(btn_style)
        newButton.setFixedSize(100, 50)
        newButton.clicked.connect(self.new)
        buttonLayout.addWidget(newButton, 0, 0)

        openButton = QPushButton('Open')
        openButton.setStyleSheet(btn_style)
        openButton.setFixedSize(100, 50)
        openButton.clicked.connect(self.open)
        buttonLayout.addWidget(openButton, 0, 1)

        saveButton = QPushButton('Save')
        saveButton.setStyleSheet(btn_style)
        saveButton.setFixedSize(100, 50)
        saveButton.clicked.connect(self.save)
        buttonLayout.addWidget(saveButton, 0, 2)

        findButton = QPushButton('Find')
        findButton.setStyleSheet(btn_style)
        findButton.setFixedSize(100, 50)
        findButton.clicked.connect(self.find)
        buttonLayout.addWidget(findButton, 0, 3)

    def new(self):
        if self.textEdit.toPlainText():
            reply = QMessageBox.question(self, 'Notepad', 'Do you want to save changes?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save()
            elif reply == QMessageBox.Cancel:
                return
        self.textEdit.clear()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def find(self):
        text, ok = QInputDialog.getText(self, 'Find Text', 'Find:')
        if ok:
            cursor = self.textEdit.document().find(text)
            if not cursor.isNull():
                cursor.select(cursor.WordUnderCursor)
                self.textEdit.setTextCursor(cursor)
            else:
                QMessageBox.information(self, '', 'Text not found.', QMessageBox.Ok)