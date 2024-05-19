import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from src.directory import Directory
from src.qt.main_window import MainWindow
from src.qt.flowlayout import FlowLayout
import random
import globals

from PIL import (
    Image,
    ImageChops,
    UnidentifiedImageError,
    ImageQt,
    ImageDraw,
    ImageFont,
    ImageEnhance,
    ImageOps,
    ImageFile,
)

import math

class ThumbnailRenderer(QObject):

    def __init__(self):
        super().__init__()

    def render(self, path, extension, base_size):

        pixelRatio = 1.0
        adj_size = 1

        try:
            if(extension in globals.IMAGES):
                image = Image.open(path)

                if image.mode == "RGBA":
                    # logging.info(image.getchannel(3).tobytes())
                    new_bg = Image.new("RGB", image.size, color="#1e1e1e")
                    new_bg.paste(image, mask=image.getchannel(3))
                    image = new_bg
                if image.mode != "RGB":
                    image = image.convert(mode="RGB")

                image = ImageOps.exif_transpose(image)

                adj_size = math.ceil(base_size * pixelRatio)

                orig_x, orig_y = image.size
                new_x, new_y = (adj_size, adj_size)

                if orig_x > orig_y:
                    new_x = adj_size
                    new_y = math.ceil(adj_size * (orig_y / orig_x))
                elif orig_y > orig_x:
                    new_y = adj_size
                    new_x = math.ceil(adj_size * (orig_x / orig_y))     

                image = image.resize((new_x, new_y), resample=Image.Resampling.BILINEAR)

                qim = ImageQt.ImageQt(image)

                if image:
                    image.close()

                _image = QPixmap.fromImage(qim)
                _image.setDevicePixelRatio(3)

            else:
                _image = QPixmap("images/No_image_available.png")
        except:
            _image = QPixmap()
            print("Failed.")
        
        return _image

