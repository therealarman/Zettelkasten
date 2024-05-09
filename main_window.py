import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# from PyQt6.QtCore import Qt, QSize, QObject, QThread, QRect
from PyQt6.QtGui import *
# from PyQt6.QtGui import QIcon, QCursor, QFont

import sys

""" VERSION NUMBER """
VERSION_NUMBER: str = '1.0.0' # Major | Minor | Patch

class Zettlekasten(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        self.setWindowTitle(f'Zettlekasten {VERSION_NUMBER}')
        self.setMinimumSize(QSize(900, 506))
        self.resize(1300, 720)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        file_menu.addAction(open_action)

        splitter_container = QWidget(self.centralWidget)
        splitter_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create three widgets for left, middle, and right sections
        left_widget = QWidget()
        middle_widget = QWidget()
        right_widget = QWidget()

        left_widget.setStyleSheet("background-color: lightblue;")
        middle_widget.setStyleSheet("background-color: lightgreen;")
        right_widget.setStyleSheet("background-color: lightcoral;")

        left_widget.setMinimumSize(200, 100)  # Adjust these sizes as needed
        middle_widget.setMinimumSize(400, 100)  # Adjust these sizes as needed
        right_widget.setMinimumSize(200, 100)  # Adjust these sizes as needed

        # Create layouts for left, middle, and right sections
        left_layout = QVBoxLayout(left_widget)
        middle_layout = QVBoxLayout(middle_widget)
        right_layout = QVBoxLayout(right_widget)

        # Create a splitter
        splitter = QSplitter()
        splitter.setHandleWidth(20)

        # Add the widgets to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(middle_widget)
        splitter.addWidget(right_widget)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setCollapsible(2, False)

        # Set the stretch factors for the widgets
        splitter.setStretchFactor(0, 1)  # Left widget
        splitter.setStretchFactor(1, 2)  # Middle widget
        splitter.setStretchFactor(2, 1)  # Right widget

        # Set the main window's central widget as the splitter
        # self.setCentralWidget(splitter)

        splitter_container_layout = QVBoxLayout(splitter_container)
        splitter_container_layout.addWidget(splitter)

        self.layout.addWidget(splitter_container)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("fusion")

    gui = Zettlekasten()
    gui.show()
    sys.exit(app.exec())