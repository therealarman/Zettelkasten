# from PyQt6.QtCore import Qt, QSize, QObject, QThread, QRect
# from PyQt6.QtGui import QIcon, QCursor, QFont

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.qt.flowlayout import FlowLayout
from src.directory import Directory

import sys
import pandas as pd
import os

""" VERSION NUMBER """
VERSION_NUMBER: str = '1.0.0' # Major | Minor | Patch

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_UI()

    def setup_UI(self):
        self.setWindowTitle(f'Zettlekasten {VERSION_NUMBER}')
        self.setMinimumSize(QSize(1300, 720))
        self.resize(1300, 920)

        self.centralWidget = QWidget(self)

        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout = QHBoxLayout()

        self.splitter = QSplitter()
        self.splitter.setHandleWidth(12)

        self.vaultSelector = QWidget()
        self.vaultSelector.setGeometry(QRect(0, 0, 300, 720))
        self.vaultSelectorLayout = QHBoxLayout(self.vaultSelector)

        self.mid_container = QWidget()
        self.mid_layout = QGridLayout(self.mid_container)
        self.mid_layout.setContentsMargins(10, 10, 10, 10)
        self.mid_layout.setSpacing(10)

        self.frame_container = QWidget()
        self.frame_layout = QVBoxLayout(self.frame_container)
        self.frame_layout.setSpacing(0)

        # ==================================
        # Add grid within frame_layout
        # ==================================

        self.scrollArea = QScrollArea()
        self.scrollArea.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 676, 720))
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.frame_layout.addWidget(self.scrollArea)

        # ==================================

        self.horizontalLayout_2 = QHBoxLayout()

        self.backButton = QPushButton(self.centralWidget)
        self.backButton.setMinimumSize(QSize(0, 32))
        self.backButton.setMaximumSize(QSize(32, 16777215))

        self.forwardButton = QPushButton(self.centralWidget)
        self.forwardButton.setMinimumSize(QSize(0, 32))
        self.forwardButton.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout_2.addWidget(self.backButton)
        self.horizontalLayout_2.addWidget(self.forwardButton)
        self.horizontalLayout_2.addStretch(1)

        self.searchField = QLineEdit(self.centralWidget)
        self.searchField.setMinimumSize(QSize(200, 32))
        self.searchField.setMaximumSize(QSize(200, 32))

        self.horizontalLayout_2.addWidget(self.searchField)

        self.mid_layout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.mid_layout.addWidget(self.frame_container, 5, 0, 1, 1)
        
        self.preview_container = QWidget()
        # self.preview_container.setGeometry(QRect(0, 0, 290, 720))
        self.preview_layout = QHBoxLayout(self.preview_container)
        self.preview_layout.setSpacing(0)
        self.preview_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.splitter)

        self.splitter.addWidget(self.vaultSelector)
        self.splitter.addWidget(self.mid_container)
        self.splitter.addWidget(self.preview_container)
        
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 1)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)

        self.vaultSelector.setMinimumSize(300, 100)  
        self.mid_container.setMinimumSize(676, 100)
        self.preview_container.setMinimumSize(300, 100)

        self.preview_container.setMaximumWidth(500)

        self.gridLayout.addLayout(self.horizontalLayout, 10, 0, 1, 1)

        self.setCentralWidget(self.centralWidget)

        # self.vaultSelector.setStyleSheet('background:lightgreen;')
        # self.scrollAreaWidgetContents.setStyleSheet('background:blue;')
        # self.mid_container.setStyleSheet('background:lightcoral;')
        # self.frame_container.setStyleSheet('background:white;')
        # self.preview_container.setStyleSheet('background:lightblue;')

    def setMenu(self):
        menu = self.menuBar()
        self.file_menu = menu.addMenu("File")
        self.edit_menu = menu.addMenu("Edit")
        self.view_menu = menu.addMenu("View")
        self.tool_menu = menu.addMenu("Tools")
        self.help_menu = menu.addMenu("Help")

        self.select_action = QAction("Select Directory", self)
        
        self.file_menu.addAction(self.select_action)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("fusion")

    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())