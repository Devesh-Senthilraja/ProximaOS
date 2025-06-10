from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QFileDialog
from PyQt5.QtCore import QDir
import vlc
import sys

class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QGridLayout(self)
        main_layout.setSpacing(15)

        self.vlcInstance = vlc.Instance()
        self.mediaPlayer = self.vlcInstance.media_player_new()

        self.videoFrame = QWidget(self)
        self.videoFrame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.videoFrame.setFixedSize(1105, 635)
        self.videoFrame.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")

        if sys.platform.startswith('linux'):
            self.mediaPlayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32":
            self.mediaPlayer.set_hwnd(self.videoFrame.winId())

        main_layout.addWidget(self.videoFrame, 0, 0, 1, 4)

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"
        buttons_layout = QGridLayout()

        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 50)
        browse_button.clicked.connect(self.open_video)
        browse_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(browse_button, 0, 0)

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setFixedSize(100, 50)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(self.play_pause_button, 0, 1)

        volume_up_button = QPushButton("Volume Up")
        volume_up_button.setFixedSize(160, 50)
        volume_up_button.clicked.connect(self.volume_up)
        volume_up_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(volume_up_button, 0, 2)

        volume_down_button = QPushButton("Volume Down")
        volume_down_button.setFixedSize(160, 50)
        volume_down_button.clicked.connect(self.volume_down)
        volume_down_button.setStyleSheet(btn_style)
        buttons_layout.addWidget(volume_down_button, 0, 3)

        main_layout.addLayout(buttons_layout, 1, 0, 1, 4)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if file_path:
            media = self.vlcInstance.media_new(file_path)
            self.mediaPlayer.set_media(media)
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def toggle_play_pause(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.play_pause_button.setText("Play")
        else:
            self.mediaPlayer.play()
            self.play_pause_button.setText("Pause")

    def volume_up(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(min(volume + 10, 100))

    def volume_down(self):
        volume = self.mediaPlayer.audio_get_volume()
        self.mediaPlayer.audio_set_volume(max(volume - 10, 0))