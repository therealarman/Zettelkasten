import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.directory import Directory
from src.qt.main_window import MainWindow
from src.qt.flowlayout import FlowWidget
from src.qt.widgets.thumb_renderer import ThumbnailRenderer
from utils import new_wrap_text

import typing

class ThumbnailButton(FlowWidget):

    small_text_style = (
        f"background-color:rgba(0, 0, 0, 192);"
        f"font-family:Oxanium;"
        f"font-weight:bold;"
        f"font-size:12px;"
        f"border-radius:3px;"
        f"padding-top: 1px;"
        f"padding-right: 1px;"
        f"padding-bottom: 1px;"
        f"padding-left: 1px;"
    )

    def __init__(self, thumb_size: tuple[int, int], fileInfo, index):
        
        super().__init__()

        self.thumb_size: tuple[int, int] = thumb_size
        self.title, self.location, self.extension = self.fileParse(fileInfo)
        self.index = index
        # print(index)
        # self.setMaximumSize(QSize(*thumb_size))
        # self.setMinimumSize(QSize(*thumb_size))

        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)

        self.thumb_button = QPushButton()
        self.thumb_button.setMaximumSize(QSize(*thumb_size))
        self.thumb_button.setMinimumSize(QSize(*thumb_size))
        self.thumb_button.setFlat(True)
        self.base_layout.addWidget(self.thumb_button)

        self.button_layout = QVBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_button.setLayout(self.button_layout)

        self.renderer = ThumbnailRenderer()

        self.renderer.updated.connect(
            lambda i: (
                self.update_thumbnail(img=i)
            )
        )

        # thmbImg = self.renderer.render(self.location, self.extension, 150)
        # self.thumb_button.setIcon(QIcon(thmbImg))
        # self.thumb_button.setIconSize(QSize(*thumb_size))

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(6, 6, 6, 6)
        self.top_container = QWidget()
        self.top_container.setLayout(self.top_layout)
        self.button_layout.addWidget(self.top_container)

        self.button_layout.addStretch(2)

        # self.reassign_button_click(button=self.thumb_button, new_action=self.print_index())

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(6, 6, 6, 6)
        self.bottom_container = QWidget()
        self.bottom_container.setLayout(self.bottom_layout)
        self.button_layout.addWidget(self.bottom_container)

        self.ext_badge = QLabel()
        self.ext_badge.setStyleSheet(ThumbnailButton.small_text_style)
        self.ext_badge.setText(str(self.extension).upper())
        self.bottom_layout.addWidget(self.ext_badge)

        self.bottom_layout.addStretch(2)

        self.title_label = QLabel()
        self.title_label.setMinimumSize(150, 50)
        self.title_label.setMaximumSize(150, 50)
        self.base_layout.addWidget(self.title_label)

        # self.title_label.setStyleSheet('background:lightcoral;')

        self.wrappedTitle = new_wrap_text(self.title, self.title_label.fontMetrics(), 150, True, 2)
        # self.wrappedTitle = wrap_text(self.title, max_lines=2)
        self.title_label.setText(self.wrappedTitle)
        
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def fileParse(self, fileInfo):
        title = fileInfo[0]
        location = fileInfo[1]
        extension = fileInfo[2]

        return [title, location, extension]
    
    def reassign_button_click(self, button: QPushButton, new_action):

        try:
            # Disconnect all previous connections to the clicked signal
            self.thumb_button.clicked.disconnect()
        except TypeError:
            # This will be raised if there were no connections before
            pass
        
        # Connect the new action
        self.thumb_button.clicked.connect(new_action)

    # def print_index(self):
    #     print(self.index)

    def update_thumbnail(self, img):
        # thmbImg = self.renderer.render(self.location, self.extension, 150)
        self.thumb_button.setIcon(QIcon(img))
        self.thumb_button.setIconSize(QSize(*self.thumb_size))