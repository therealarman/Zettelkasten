import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import typing
import pandas as pd

from src.qt.widgets.thumb_renderer import ThumbnailRenderer
from utils import wrap_text

if typing.TYPE_CHECKING:
    from src.qt.zettelkasten import Zettelkasten

class PreviewWidget(QWidget):

    # title_text_style = (
    #     f"background-color:rgba(0, 0, 0, 192);"
    #     f"font-family:Oxanium;"
    #     f"font-weight:bold;"
    #     f"font-size:12px;"
    #     f"border-radius:3px;"
    #     f"padding-top: 1px;"
    #     f"padding-right: 1px;"
    #     f"padding-bottom: 1px;"
    #     f"padding-left: 1px;"
    # )

    # subtitle_text_style = (
    #     f"background-color:rgba(0, 0, 0, 192);"
    #     f"font-family:Oxanium;"
    #     f"font-weight:bold;"
    #     f"font-size:12px;"
    #     f"border-radius:3px;"
    #     f"padding-top: 1px;"
    #     f"padding-right: 1px;"
    #     f"padding-bottom: 1px;"
    #     f"padding-left: 1px;"
    # )

    def __init__(self, thumb_size: tuple[int, int], main_driver: "Zettelkasten"):
        
        super().__init__()

        self.thumb_size: tuple[int, int] = thumb_size
        self.driver = main_driver
        self.image_ratio: float = 1.0
        self.renderer = ThumbnailRenderer()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_img = QPushButton()
        self.preview_img.setFlat(True)
        self.preview_img.setMinimumSize(QSize(*thumb_size))

        self.file_label = QLabel("Bluelock.png")
        self.file_label.setStyleSheet("font-weight: bold; font-size: 12px")

        image_layout.addWidget(self.preview_img)
        image_layout.setAlignment(self.preview_img, Qt.AlignmentFlag.AlignCenter)

        self.title_container = QWidget()
        title_layout = QVBoxLayout(self.title_container)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-weight: bold; font-size: 25px")

        self.dir_label = QLabel()
        self.dir_label.setStyleSheet("font-weight: light,; font-size: 12px")

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.dir_label)

        image_layout.addWidget(self.title_container)
        self.title_container.setMaximumWidth(280)
        self.title_container.setMinimumWidth(280)
        image_layout.setAlignment(self.title_container, Qt.AlignmentFlag.AlignCenter)

        # image_layout.addStretch(2)

        # self.title_container.setStyleSheet('background:lightblue;')
        # self.preview_img.setStyleSheet('background:lightcoral;')

        root_layout.addWidget(self.image_container)

        root_layout.addStretch(2)

        self.metadata_container = QWidget()
        self.metadata_container.setMaximumWidth(280)
        self.metadata_container.setMinimumWidth(280)
        metadata_layout = QFormLayout(self.metadata_container)

        root_layout.addWidget(self.metadata_container)

        # self.metadata_container.setStyleSheet('background:lightcoral;')


    def update_widget(self):

        if self.driver.selected:
            self.selected = self.driver.selected[0]

            title, location, ext = self.driver.lib.dataframe.loc[self.selected, ["Title", "Location", "Type"]]

            selected_img = self.renderer.render(location, ext, self.thumb_size[0])

            self.preview_img.setIcon(QIcon(selected_img))

            self.title_label.setText(wrap_text(title, 17, max_lines=2))
            self.dir_label.setText(wrap_text(location, width=43, max_lines=4))

        else:
            self.selected = None

        self.update_image_size(
            (self.thumb_size[0], self.thumb_size[1])
        )



    def resizeEvent(self, event: QResizeEvent) -> None:
        # self.update_image_size(
        #     (self.image_container.size().width(), self.image_container.size().height())
        # )

        self.update_image_size(
            (self.thumb_size[0], self.thumb_size[1])
        )

        return super().resizeEvent(event)

    def set_image_ratio(self, ratio: float):
        # logging.info(f'Updating Ratio to: {ratio} #####################################################')
        self.image_ratio = ratio

    def update_image_size(self, size: tuple[int, int], ratio: float = None):
        if ratio:
            self.set_image_ratio(ratio)
        # self.img_button_size = size
        # logging.info(f'')
        # self.preview_img.setMinimumSize(64,64)

        adj_width: float = size[0]
        adj_height: float = size[1]
        # Landscape
        if self.image_ratio > 1:
            # logging.info('Landscape')
            adj_height = size[0] * (1 / self.image_ratio)
        # Portrait
        elif self.image_ratio <= 1:
            # logging.info('Portrait')
            adj_width = size[1] * self.image_ratio

        if adj_width > size[0]:
            adj_height = adj_height * (size[0] / adj_width)
            adj_width = size[0]
        elif adj_height > size[1]:
            adj_width = adj_width * (size[1] / adj_height)
            adj_height = size[1]

        adj_size = QSize(int(adj_width), int(adj_height))
        self.img_button_size = (int(adj_width), int(adj_height))
        # self.preview_img.setMinimumSize(adj_size)
        self.preview_img.setMaximumSize(adj_size)
        self.preview_img.setIconSize(adj_size)