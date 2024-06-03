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
from src.qt.widgets.preview_widget import PreviewWidget

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
        self.thumbnails: list[ThumbnailButton] = []
        self.selected = []

        menu = self.MainWindow.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.edit_menu = menu.addMenu("&Edit")
        self.view_menu = menu.addMenu("&View")
        self.tool_menu = menu.addMenu("&Tools")
        self.help_menu = menu.addMenu("&Help")

        self.open_action = QAction("&Open/Create Library", self)
        self.open_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_action.triggered.connect(self.open_file_dialog)
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction("&Save Library", self)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_action.triggered.connect(self.save_library)
        self.file_menu.addAction(self.save_action)

        self.reload_action = QAction("&Refresh Library", self)
        self.reload_action.setShortcut(QKeySequence("Ctrl+R"))
        self.reload_action.triggered.connect(self.refresh_library)
        self.file_menu.addAction(self.reload_action)

        self.preview_panel = PreviewWidget((280, 280), main_driver=self)
        self.MainWindow.preview_layout.addWidget(self.preview_panel)

        self.MainWindow.show()

        # sys.exit(app.exec())
        app.exec()
        self.shutdown()

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
        self.flow_container.setLayout(layout)

        self.thumbnails.clear()

        for idx, i in enumerate(entries):
            thumbnail = ThumbnailButton((150, 150), i, idx)
            layout.addWidget(thumbnail)            
            self.thumbnails.append(thumbnail)
                        
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sa: QScrollArea = self.MainWindow.scrollArea
        sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sa.setWidgetResizable(True)
        sa.setWidget(self.flow_container)

        for i in self.thumbnails:

            i.reassign_button_click(
                button=i.thumb_button, 
                new_action=(lambda checked=False, index_to_pass=i.index: self.select_thumb(id=index_to_pass))
                )

    def save_library(self):

        # TODO: Check if .Zettlekasten folder has been moved / Check if home directory still exists.
        # If not, prompt dialogue for new save location

        if self.lib.current_dir:
            self.lib.save_library()

    def refresh_library(self):

        if self.lib.current_dir:
            self.lib.populate_library()

            df = self.lib.dataframe
            names_list = df.apply(lambda row: [row['Title'], row['Location'], row['Type']], axis=1).tolist()

            layout = FlowLayout()
            layout.setSpacing(8)

            self.init_thumbnail_grid(names_list, layout)

    def shutdown(self):
        """Save Library on Application Exit"""
        if self.lib.current_dir:
            self.save_library()

        QApplication.quit()

    def select_thumb(self, id: int):

        if id not in self.selected:
            self.selected.clear()
            self.selected.append(id)
            # print(f"Selected {id}")
            # for it in self.item_thumbs:
                # if it.mode == type and it.item_id == id:
                    # it.thumb_button.set_selected(True)
        else:
            self.selected.remove(id)
            # print(f"Deselected {id}")
            # for it in self.item_thumbs:
                # if it.mode == type and it.item_id == id:
                    # it.thumb_button.set_selected(False)

        self.preview_panel.update_widget()