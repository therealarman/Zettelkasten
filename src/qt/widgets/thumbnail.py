import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.directory import Directory
from src.qt.main_window import MainWindow
from src.qt.flowlayout import FlowLayout
import random
import globals

class ThumbnailButton(QWidget):

    small_text_style = (
        # f"background-color:rgba(0, 0, 0, 192);"
        f"background-color:rgba(20, 139, 228, 192);"
        f"font-family:Oxanium;"
        f"font-weight:bold;"
        f"font-size:12px;"
        f"border-radius:3px;"
        f"padding-top: 2px;"
        f"padding-right: 1px;"
        # f"padding-bottom: 1px;"
        f"padding-left: 1px;"
    )

    # def __init__(self, title: str, _s: int, image: QPixmap, flowLayout: FlowLayout):
    def __init__(self, fileInfo, _s: int, flowLayout: FlowLayout):
        super().__init__()

        # self.title = self.adjustTitleLength(title)
        self.title, self.location, self.extension = self.fileParse(fileInfo)
        # self._s = _s
        # self.image = image
        self.flowLayout = flowLayout

        self.setup_ui()

    def setup_ui(self):

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QFrame(self)
        self.layout.addWidget(self.frame)

        self.thumbnail_button = QPushButton()
        self.layout.addWidget(self.thumbnail_button)
        self.thumbnail_button.setMinimumSize(150, 150)
        self.thumbnail_button.setMaximumSize(150, 150)
        self.thumbnail_button.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.thumbnail_button.setFlat(False)

        self.extension_label = QLabel()
        self.layout.addWidget(self.extension_label)
        self.extension_label.setStyleSheet(self.small_text_style)
        self.extension_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.extension_label.setMaximumSize(35, 18)
        self.extension_label.setMinimumSize(5, 18)
        self.extension_label.setText(str(self.extension).upper())
        self.extension_label.adjustSize()

        self.title_label = QLabel()
        self.layout.addWidget(self.title_label)
        self.title_label.setMinimumSize(150, 15)
        self.title_label.setMaximumSize(150, 30)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)

        self.title_label.setText(self.title)

        if (self.extension).lower() in globals.IMAGES:
            self.thumbnail_button.setStyleSheet("background:lightcoral;")

        # size = QSize(self._s, self._s)

        # ico_size = self.maximizeIcon(self.image, self._s)

        # self.thumbnail_button.setIcon(QIcon(self.image))
        # self.thumbnail_button.setIconSize(ico_size)

    def maximizeIcon(self, pixmap: QPixmap, max_size: int):
        original_width = pixmap.width()
        original_height = pixmap.height()

        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(new_height * aspect_ratio)

        return QSize(new_width, new_height)
    
    def adjustTitleLength(self, title: str):

        max_len = 10

        truncated = title[:max_len] + "..." if (len(title) > max_len) else title

        return truncated

    def fileParse(self, fileInfo):
        title = fileInfo[0]
        location = fileInfo[1]
        extension = fileInfo[2]

        return [title, location, extension]

