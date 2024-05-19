import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.directory import Directory
from src.qt.main_window import MainWindow
from src.qt.flowlayout import FlowLayout
import random
import globals
from src.qt.widgets.thumb_renderer import ThumbnailRenderer
from utils import wrap_text

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
    def __init__(self, fileInfo, _s: int):
        super().__init__()

        # self.title = self.adjustTitleLength(title)
        self.title, self.location, self.extension = self.fileParse(fileInfo)
        # self.extension = self.extension.upper()
        # self._s = _s
        # self.image = image
        self.setup_ui()

    def setup_ui(self):

        # self.setMaximumSize(150, 215)
        # self.setMinimumSize(150, 215)

        self.setFixedSize(150, 215)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

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
        self.title_label.setMinimumSize(150, 35)
        self.title_label.setMaximumSize(150, 35)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wrappedTitle = wrap_text(self.title, max_lines=2)
        self.title_label.setText(self.wrappedTitle)
        
        # if (self.extension).lower() in globals.IMAGES:
            # self.thumbnail_button.setStyleSheet("background:lightcoral;")
        self.thumbnail_button.setStyleSheet("background:lightcoral;")
        
        self.renderer = ThumbnailRenderer()

        thmbImg = self.renderer.render(self.location, self.extension, 120)

        self.thumbnail_button.setIcon(QIcon(thmbImg))
        self.thumbnail_button.setIconSize(QSize(120, 120))

    def fileParse(self, fileInfo):
        title = fileInfo[0]
        location = fileInfo[1]
        extension = fileInfo[2]

        return [title, location, extension]

