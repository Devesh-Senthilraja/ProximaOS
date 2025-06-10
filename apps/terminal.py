from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import subprocess

class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        controls = QGridLayout()
        layout.addLayout(controls, 0, 0)

        address_label = QLabel("ProximaOS:~", self)
        address_label.setStyleSheet("font: bold 15px 'Arial';")
        controls.addWidget(address_label, 0, 0)

        self.commandLine = QLineEdit(self)
        self.commandLine.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.commandLine.setFixedSize(900, 50)
        controls.addWidget(self.commandLine, 0, 1)

        runButton = QPushButton("Run", self)
        runButton.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        runButton.setFixedSize(100, 50)
        runButton.clicked.connect(self.runCommand)
        controls.addWidget(runButton, 0, 2)

        viewer = QTextEdit(self)
        viewer.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        viewer.setFixedSize(1105, 645)
        layout.addWidget(viewer, 1, 0)

        self.commandOutput = viewer

    def runCommand(self):
        command = self.commandLine.text()
        self.commandLine.clear()

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.commandOutput.append("ProximaOS:~ " + command)

        cmdResults, cmdErrors = process.communicate()
        if cmdResults:
            self.commandOutput.append(cmdResults.decode())
        if cmdErrors:
            self.commandOutput.append(cmdErrors.decode())