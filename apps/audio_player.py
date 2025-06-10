from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDir
import vlc

class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(15)

        thumbnail = QLabel(self)
        thumbnail.setFixedSize(625, 560)
        thumbnail.setStyleSheet("background-color: #f0f0f0; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        pixmap = QPixmap("audio.png")
        scaled_pixmap = pixmap.scaled(thumbnail.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        thumbnail.setPixmap(scaled_pixmap)
        grid_layout.addWidget(thumbnail, 0, 0, 1, 4)

        self.vlcInstance = vlc.Instance()
        self.mediaPlayer = self.vlcInstance.media_player_new()

        btn_style = "background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;"
        button_layout = QGridLayout()

        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 50)
        browse_button.clicked.connect(self.open_audio)
        browse_button.setStyleSheet(btn_style)
        button_layout.addWidget(browse_button, 0, 0)

        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.setFixedSize(100, 50)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(btn_style)
        button_layout.addWidget(self.play_pause_button, 0, 1)

        volume_up_button = QPushButton("Volume Up")
        volume_up_button.setFixedSize(160, 50)
        volume_up_button.clicked.connect(self.volume_up)
        volume_up_button.setStyleSheet(btn_style)
        button_layout.addWidget(volume_up_button, 0, 2)

        volume_down_button = QPushButton("Volume Down")
        volume_down_button.setFixedSize(160, 50)
        volume_down_button.clicked.connect(self.volume_down)
        volume_down_button.setStyleSheet(btn_style)
        button_layout.addWidget(volume_down_button, 0, 3)

        grid_layout.addLayout(button_layout, 1, 0, 1, 4)

    def open_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio", QDir.homePath(), "Audio Files (*.mp3 *.wav *.flac)")
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