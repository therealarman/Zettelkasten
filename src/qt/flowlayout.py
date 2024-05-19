"""PySide6 port of the widgets/layouts/flowlayout example from Qt v6.x"""

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class FlowWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ignore_size: bool = False

class FlowLayout(QLayout):

    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []
        self.free_space = 150

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        all_rows_list = []
        row_list = []

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical
            )
            space_x = spacing + layout_spacing_x
            # space_y = spacing
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

                all_rows_list.append(row_list)
                row_list = []
                row_list.append(item)
            else:
                row_list.append(item)

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))  

            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        
        # if(len(all_rows_list) > 0):
        #     max_in_row = len(all_rows_list[0])
        #     occupied_space = spacing * (max_in_row)
        #     line_width = rect.right() - rect.left()
        #     self.free_space = (line_width - occupied_space) / max_in_row

        #     _ctr = 1
        #     _y = 0

        #     for item in self._item_list:

        #         if(_ctr > ((max_in_row * 2) - 1)):
        #             _ctr = 1

        #             _y += spacing + max(line_height, item.sizeHint().height())

        #         new_x = (((line_width / max_in_row) * 0.5) * _ctr) - (item.sizeHint().width() / 2)
        #         new_pos = QPoint(round(new_x), _y)
        #         # new_pos = QPoint(round(new_x), item.geometry().y())
        #         item.setGeometry(QRect(new_pos, item.sizeHint()))

        #         _ctr += 2
                
        return y + line_height - rect.y()