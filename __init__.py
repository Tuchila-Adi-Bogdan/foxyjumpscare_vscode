import sys
import os
import xml.etree.ElementTree as ET
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import QTimer, QRect, Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class JumpscarePlayer(QWidget):
    def __init__(self, xml_path, png_path, audio_path):
        super().__init__()

        # 1. SETUP WINDOW
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        # 2. LOAD VISUALS
        self.frames = self.parse_xml(xml_path)
        self.atlas_pixmap = QPixmap(png_path)
        
        if self.atlas_pixmap.isNull():
            print(f"Error: Could not load image at {png_path}")
            sys.exit(1)

        self.current_frame_index = 0
        self.total_frames = len(self.frames)
        
        # 3. SETUP AUDIO
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0) # 100% Volume
        
        # Load the file
        if os.path.exists(audio_path):
            self.media_player.setSource(QUrl.fromLocalFile(os.path.abspath(audio_path)))
            self.media_player.play()
        else:
            print(f"Error: Audio file not found at {audio_path}")

        # 4. START ANIMATION
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(40) 

    def parse_xml(self, xml_path):
        if not os.path.exists(xml_path):
            print(f"Error: XML file not found at {xml_path}")
            sys.exit(1)

        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        frames = []
        for sub_texture in root.findall('SubTexture'):
            attr = sub_texture.attrib
            data = {
                'name': attr.get('name'),
                'x': int(attr.get('x')),
                'y': int(attr.get('y')),
                'w': int(attr.get('width')),
                'h': int(attr.get('height')),
                'fx': int(attr.get('frameX', 0)),
                'fy': int(attr.get('frameY', 0)),
                'fw': int(attr.get('frameWidth', 0)),
                'fh': int(attr.get('frameHeight', 0))
            }
            if data['fw'] == 0: data['fw'] = data['w']
            if data['fh'] == 0: data['fh'] = data['h']
            frames.append(data)
            
        frames.sort(key=lambda k: k['name'])
        return frames

    def next_frame(self):
        self.current_frame_index += 1
        
        if self.current_frame_index >= self.total_frames:
            self.close()
            sys.exit()
        
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        frame_data = self.frames[self.current_frame_index]

        source_rect = QRect(
            frame_data['x'], frame_data['y'], 
            frame_data['w'], frame_data['h']
        )

        screen_w = self.width()
        screen_h = self.height()
        
        origin_x = (screen_w - frame_data['fw']) // 2
        origin_y = (screen_h - frame_data['fh']) // 2
        
        dest_x = origin_x - frame_data['fx']
        dest_y = origin_y - frame_data['fy']

        painter.drawPixmap(dest_x, dest_y, self.atlas_pixmap, 
                           source_rect.x(), source_rect.y(), source_rect.width(), source_rect.height())
        
        painter.end()

if __name__ == "__main__":
    XML_FILE = "foxy.xml" 
    PNG_FILE = "foxy.png" 
    AUDIO_FILE = "jumpscare.mp3"
    app = QApplication(sys.argv)
    player = JumpscarePlayer(XML_FILE, PNG_FILE, AUDIO_FILE)
    sys.exit(app.exec())