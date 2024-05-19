import sys

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from src.directory import Directory
from src.qt.main_window import MainWindow
from src.qt.widgets.new_thumbnail import ThumbnailButton
# from src.qt.widgets.thumbnail import ThumbnailButton
from src.qt.flowlayout import FlowLayout

class Zettelkasten(QObject):

    def __init__(self):
        super().__init__()

    def start(self):
        print("Starting...")

        app = QApplication([])
        app.setStyle("fusion")

        self.MainWindow = MainWindow()
        self.loc = ''

        # loc = 'C:/Users/Arman/Downloads'

        self.MainWindow.select_action.triggered.connect(self.openFileDialog)

        # print(self.MainWindow.devicePixelRatio())

        # thisDir = Directory(self.loc)
        # df, ls = thisDir.getFiles()

        # names_list = df[df['Type'].isin(['.png', '.jpeg', '.jpg'])].apply(lambda row: [row['Title'], row['Location']], axis=1).tolist()

        # for i in names_list:

        #     thisImg = QPixmap(i[1])

        #     thmb = ThumbnailButton(str(i[0]), 150, thisImg, self.MainWindow.flowLayout)

        #     self.MainWindow.flowLayout.addWidget(thmb)

        self.MainWindow.show()
        sys.exit(app.exec())

    def openFileDialog(self):
        file_dialog = QFileDialog(self.MainWindow)
        folder_path = file_dialog.getExistingDirectory(self.MainWindow, "Select Folder")
        
        if folder_path:
            self.loc = folder_path

            layout = FlowLayout()
            layout.setSpacing(8)

            # self.clearLayout(self.MainWindow.flowLayout)

            thisDir = Directory(self.loc)
            df, ls = thisDir.getFiles()

            # names_list = df[df['Type'].isin(['.png', '.jpeg', '.jpg'])].apply(lambda row: [row['Title'], row['Location']], axis=1).tolist()
            names_list = df.apply(lambda row: [row['Title'], row['Location'], row['Type']], axis=1).tolist()

            for i in names_list:
                thmb = ThumbnailButton((150, 150), i)
                # thmb = ThumbnailButton(i, 150)
                layout.addWidget(thmb)
            
            self.flow_container: QWidget = QWidget()
            self.flow_container .setLayout(layout)

            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sa: QScrollArea = self.MainWindow.scrollArea
            sa.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            sa.setWidgetResizable(True)
            sa.setWidget(self.flow_container)


    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

