import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import typing
import pandas as pd

from src.qt.widgets.thumb_renderer import ThumbnailRenderer
from utils import wrap_text, new_wrap_text

if typing.TYPE_CHECKING:
    from src.qt.zettelkasten import Zettelkasten

class PreviewWidget(QWidget):

    def __init__(self, thumb_size: tuple[int, int], main_driver: "Zettelkasten"):
        
        super().__init__()

        self.thumb_size: tuple[int, int] = thumb_size
        self.driver = main_driver
        self.image_ratio: float = 1.0

        self.renderer = ThumbnailRenderer()

        self.renderer.updated.connect(
            lambda i: (
                self.update_thumbnail(img=i)
            )
        )

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        image_layout.setContentsMargins(5, 5, 5, 5)

        self.preview_img = QPushButton()
        self.preview_img.setFlat(True)
        # self.preview_img.setMinimumSize(QSize(*thumb_size))
        self.preview_img.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.file_label = QLabel()
        self.file_label.setStyleSheet("font-weight: bold; font-size: 12px")

        image_layout.addWidget(self.preview_img)
        # image_layout.setAlignment(self.preview_img, Qt.AlignmentFlag.AlignCenter)

        self.title_container = QWidget()
        title_layout = QVBoxLayout(self.title_container)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-weight: bold; font-size: 25px")
        

        self.t_font = self.title_label.font()
        self.t_font.setBold(True)
        self.t_font.setPixelSize(25)
        self.t_font_metric = QFontMetrics(self.t_font)

        # 67 11 6


        self.dir_label = QLabel()
        self.dir_label.setStyleSheet("font-weight: light,; font-size: 12px")

        self.d_font = self.dir_label.font()
        self.d_font.setBold(False)
        self.d_font.setPixelSize(12)
        self.d_font_metric = QFontMetrics(self.d_font)


        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.dir_label)

        image_layout.addWidget(self.title_container)


        root_layout.addWidget(self.image_container)

        root_layout.addStretch(2)

        self.metadata_container = QWidget()
        self.metadata_container.setMaximumWidth(280)
        self.metadata_container.setMinimumWidth(280)
        metadata_layout = QFormLayout(self.metadata_container)

        root_layout.addWidget(self.metadata_container)

        # self.title_container.setStyleSheet('background:lightblue;')
        # self.metadata_container.setStyleSheet('background:lightcoral;')
        # self.image_container.setStyleSheet('background:lightgreen')


    def update_widget(self):

        adj_container_width = self.image_container.width() - 10

        if self.driver.selected:
            self.selected = self.driver.selected[0]

            title, location, ext = self.driver.lib.dataframe.loc[self.selected, ["Title", "Location", "Type"]]

            self.renderer.render(location, ext, 500)


            # selected_img = self.renderer.render(location, ext, 500)
            # self.preview_img.setIcon(QIcon(selected_img))

            self.title_label.setText(new_wrap_text(title, self.t_font_metric, adj_container_width))
            self.dir_label.setText(new_wrap_text(location, self.d_font_metric, adj_container_width, True))

        else:
            self.selected = None

            self.preview_img.setIcon(QIcon())
            self.title_label.setText("")
            self.dir_label.setText("")

        self.update_image_size(
            (adj_container_width, adj_container_width)    
        )



    def resizeEvent(self, event: QResizeEvent) -> None:

        adj_container_width = self.image_container.width() - 10

        if self.driver.selected:
            title, location, ext = self.driver.lib.dataframe.loc[self.selected, ["Title", "Location", "Type"]]
            self.title_label.setText(new_wrap_text(title, self.t_font_metric, adj_container_width))
            self.dir_label.setText(new_wrap_text(location, self.d_font_metric, adj_container_width, True))

            # print(new_wrap_text(location, self.d_font_metric, adj_container_width, True))

        self.update_image_size(
            (adj_container_width, adj_container_width)
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

        adj_size = QSize(int(adj_width), int(adj_width))

        # adj_size = QSize(int(adj_width), int(adj_height))
        # self.img_button_size = (int(adj_width), int(adj_height))
        self.img_button_size = (int(adj_width), int(adj_width))
        
        self.preview_img.setMaximumSize(adj_size)
        self.preview_img.setIconSize(adj_size)

        # print(f"Width: {adj_width}")

    def update_thumbnail(self, img):
        self.preview_img.setIcon(QIcon(img))