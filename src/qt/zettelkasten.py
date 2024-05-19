import sys

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.directory import Directory
from src.library import Library
from src.qt.main_window import MainWindow
from src.qt.flowlayout import FlowLayout
from src.qt.widgets.thumbnail import ThumbnailButton

class Zettelkasten(QObject):

    def __init__(self):
        super().__init__()

    def start(self):
        print("Starting...")

        app = QApplication([])
        app.setStyle("Fusion")

        self.MainWindow = MainWindow()
        self.loc = ''
        self.lib = Library()
        # self.loc = 'C:/Users/Arman/Downloads'

        menu = self.MainWindow.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.edit_menu = menu.addMenu("&Edit")
        self.view_menu = menu.addMenu("&View")
        self.tool_menu = menu.addMenu("&Tools")
        self.help_menu = menu.addMenu("&Help")

        self.open_action = QAction("&Open/Create Library", self)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.open_action)

        # self.open_action.setShortcut(QKeySequence(Qt.Key.Key_Control, Qt.Key.Key_O))
        # self.open_action.setToolTip("Ctrl+O")

        self.save_action = QAction("&Save Library", self)
        self.save_action.triggered.connect(self.save_library)
        self.file_menu.addAction(self.save_action)

        self.save_action = QAction("&Refresh Library", self)
        self.save_action.triggered.connect(self.save_library)
        self.file_menu.addAction(self.save_action)

        # self.MainWindow.select_action.triggered.connect(self.openFileDialog)

        self.MainWindow.show()
        sys.exit(app.exec())

    def open_file_dialog(self):
        file_dialog = QFileDialog(self.MainWindow)
        folder_path = file_dialog.getExistingDirectory(self.MainWindow, "Select Folder")
        
        if folder_path:
            self.loc = folder_path

            layout = FlowLayout()
            layout.setSpacing(8)

            self.open_library(self.loc)
            df = self.lib.dataframe

            names_list = df.apply(lambda row: [row['Title'], row['Location'], row['Type']], axis=1).tolist()

            self.init_thumbnail_grid(names_list, layout)

    def open_library(self, path):
        
        if self.lib.current_dir:
            self.lib.save_library()
            self.lib.clear_variables()
        
        return_code = self.lib.open_library(path)

        print(return_code)

        if return_code == 1:
            pass
        else:
            print("Creating New Library")
            self.lib.create_library(path)
            self.lib.populate_library()

    def init_thumbnail_grid(self, entries, layout):

        self.flow_container: QWidget = QWidget()
        self.flow_container .setLayout(layout)

        for i in entries:
            thmb = ThumbnailButton((150, 150), i)
            layout.addWidget(thmb)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sa: QScrollArea = self.MainWindow.scrollArea
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sa.setWidgetResizable(True)
        sa.setWidget(self.flow_container)

    def save_library(self):

        # TODO: Check if .Zettlekasten folder has been moved / Check if home directory still exists.
        # If not, prompt dialogue for new save location

        if self.lib.current_dir:
            self.lib.save_library()

    def refresh_library(self):

        if self.lib.current_dir:
            self.lib.populate_library()