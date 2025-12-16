import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt

class FullscreenPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        
        # 1. Remove window borders and set topmost
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 2. Setup Video Widget
        self._video_widget = QVideoWidget()
        self.setCentralWidget(self._video_widget)

        # 3. Setup Player
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setVideoOutput(self._video_widget)
        self._player.setAudioOutput(self._audio_output)
        
        # 4. Load Video
        self._player.setSource(QUrl.fromLocalFile(video_path))
        self._audio_output.setVolume(1.0) # Max volume
        
        # 5. Close app when video finishes
        self._player.mediaStatusChanged.connect(self.check_status)
        
        self._player.play()

    def check_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    video_path = sys.argv[1]
    window = FullscreenPlayer(video_path)
    
    # Force Fullscreen
    window.showFullScreen()
    
    sys.exit(app.exec())