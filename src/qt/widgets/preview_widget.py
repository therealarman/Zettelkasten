import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.qt.widgets.thumb_renderer import ThumbnailRenderer

class PreviewWidget(QWidget):

    def __init__(self, thumb_size: tuple[int, int]):
        
        super().__init__()

        self.thumb_size: tuple[int, int] = thumb_size
        self.image_ratio: float = 1.0

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.image_container = QWidget()
        image_layout = QHBoxLayout(self.image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_img = QPushButton()
        self.preview_img.setMinimumSize(QSize(*thumb_size))

        image_layout.addWidget(self.preview_img)
        image_layout.setAlignment(self.preview_img, Qt.AlignmentFlag.AlignCenter)

        root_layout.addWidget(self.image_container)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update_image_size(
            (self.image_container.size().width(), self.image_container.size().height())
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
        self.preview_img.setMaximumSize(adj_size)
        self.preview_img.setIconSize(adj_size)