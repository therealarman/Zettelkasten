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
        self.setMinimumSize(QSize(900, 506))
        self.resize(1300, 720)

        # self.colorSections = colorSections

        self.centralWidget = QWidget(self)

        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout = QHBoxLayout()

        self.splitter = QSplitter()
        self.splitter.setHandleWidth(12)

        self.vaultSelector = QWidget()
        self.vaultSelector.setGeometry(QRect(0, 0, 300, 590))
        # self.vaultSelector.setStyleSheet('background:lightgreen')
        self.vaultSelectorLayout = QHBoxLayout(self.vaultSelector)

        self.mid_container = QWidget()
        # self.mid_container.setStyleSheet('background:lightcoral;')
        self.mid_layout = QGridLayout(self.mid_container)
        self.mid_layout.setContentsMargins(10, 10, 10, 10)
        self.mid_layout.setSpacing(10)

        self.frame_container = QWidget()
        # self.frame_container.setStyleSheet('background:white;')
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1260, 590))

        # self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        # self.gridLayout_2.setSpacing(8)
        # self.gridLayout_2.setContentsMargins(0, 0, 0, 8)

        # self.flowLayout = FlowLayout(self.scrollAreaWidgetContents)
        # self.flowLayout.setSpacing(8)
        # self.flowLayout.setContentsMargins(0, 0, 0, 8)
        
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
        
        self.pvTest = QWidget()
        self.pvTest.setGeometry(QRect(0, 0, 300, 590))
        # self.pvTest.setStyleSheet('background:lightblue')
        self.pvTestLayout = QHBoxLayout(self.pvTest)

        self.horizontalLayout.addWidget(self.splitter)

        self.splitter.addWidget(self.vaultSelector)
        self.splitter.addWidget(self.mid_container)
        self.splitter.addWidget(self.pvTest)
        
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 1)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, False)

        self.vaultSelector.setMinimumSize(213, 100)  
        self.mid_container.setMinimumSize(450, 100)
        self.pvTest.setMinimumSize(213, 100) 

        self.gridLayout.addLayout(self.horizontalLayout, 10, 0, 1, 1)

        self.setCentralWidget(self.centralWidget)

        # if(self.colorSections == True):
        # self.vaultSelector.setStyleSheet('background:lightgreen;')
        # self.scrollAreaWidgetContents.setStyleSheet('background:blue;')
        # self.mid_container.setStyleSheet('background:lightcoral;')
        # self.frame_container.setStyleSheet('background:white;')
        # self.pvTest.setStyleSheet('background:lightblue;')

        # self.dir_search = QLineEdit(left_widget)
        # self.dir_search.setPlaceholderText("Enter a Directory")
        # self.dir_search.setMinimumSize(QSize(32, 32))
        # self.dir_search.setMaximumSize(QSize(200, 16777215))
        # left_layout.addWidget(self.dir_search)

        # self.dir_button = QPushButton("Search", left_widget)
        # self.dir_button.clicked.connect(self.on_search_clicked)
        # self.dir_button.setMinimumSize(QSize(32, 32))
        # self.dir_button.setMaximumSize(QSize(200, 16777215))
        # left_layout.addWidget(self.dir_button)

        # self.fileShow = QLabel("...", middle_widget)
        # middle_layout.addWidget(self.fileShow)

    # def on_search_clicked(self):
    #     loc_string = self.dir_search.text().replace(os.sep, '/')
    #     thisDir = Directory(loc_string)

    #     df, ls = thisDir.getFiles()

    #     self.fileShow.setText(str(df.head(10)))

        # self.setMenu()

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