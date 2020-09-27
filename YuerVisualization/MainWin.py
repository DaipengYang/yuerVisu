import os
import cv2
import numpy as np
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QDockWidget
from PyQt5.QtWidgets import QLabel, QSpinBox, QPushButton, QScrollArea
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from canvasvideo import CentralWindow
from toolbar import new_action, add_actions, ToolBar, ActionDict


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(600, 400)

        ##### --Layout start-- #####
        # --left-- #
        self.file_list = QListWidget()
        self.file_list.setMaximumWidth(200)
        self.file_list_label = QLabel('Images list')
        left_vbox_layout = QVBoxLayout()
        left_vbox_layout.addWidget(self.file_list_label)
        left_vbox_layout.addWidget(self.file_list)
        left_container = QWidget()
        left_container.setLayout(left_vbox_layout)
        self.file_list_dock = QDockWidget()
        self.file_list_dock.setWidget(left_container)
        # --central-- #
        self.central_window = CentralWindow()
        # Set the central widget.
        self.setCentralWidget(self.central_window)
        # Set the dock areas for dock widget.
        self.file_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.file_list_dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_list_dock)
        ##### --Layout end-- #####

        ##### --Widget slot start-- #####
        self.file_list.doubleClicked.connect(self.file_list_double_clicked)
        ##### --Widget slot end-- #####

        ##### --Toolbar and toolbar action start-- #####
        p_action = partial(new_action, self)
        open_image = p_action('&Open file', self.a_open_file, 'Ctrl+o', 'open', 'Open image or directory.')
        open_next_image = p_action('&Next file', self.a_open_next_file, 'Ctrl+n', 'next', 'Open next image.')
        open_prev_image = p_action('&Prev file', self.a_open_prev_file, 'Ctrl+p', 'prev', 'Open prev image.')
        self.toolbar = ToolBar('ToolBar')
        self.actions = ActionDict(open_image=open_image,
                                  open_next_image=open_next_image,
                                  open_prev_image=open_prev_image)
        add_actions(self.toolbar, (None, open_image, open_next_image, open_prev_image, None))
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        ##### --Toolbar and toolbar action end-- #####

        ##### --Initial state start-- #####
        self.file_filters = ['.jpg', '.JPG', '.jpeg', '.png', '.bmp']
        self.file_dir = os.getcwd()
        self.filename_current = 'default.png'
        self.filenames = []
        ##### --Initial state end-- #####

        self.load_file(os.path.join(self.file_dir, self.filename_current))

    def a_open_file(self):
        filters = 'Image files (*%s)' % ' *'.join(self.file_filters)
        filename = QFileDialog.getOpenFileName(self, 'Choose image file.', filter=filters)
        if filename[0]:
            self.load_file(filename[0])

    def a_open_next_file(self):
        idx_cur = self.filenames.index(self.filename_current)
        idx = idx_cur + 1
        if idx >= len(self.filenames):
            return
        # --Update file_list start-- #
        self.filename_current = self.filenames[idx]
        self.file_list.setCurrentRow(idx)
        # --Update file_list end-- #
        self.load_image()

    def a_open_prev_file(self):
        idx_cur = self.filenames.index(self.filename_current)
        idx = idx_cur - 1
        if idx < 0:
            return
        # --Update file_list start-- #
        self.filename_current = self.filenames[idx]
        self.file_list.setCurrentRow(idx)
        # --Update file_list end-- #
        self.load_image()

    def file_list_double_clicked(self):
        idx_cur = self.file_list.currentRow()
        if self.filename_current == self.filenames[idx_cur]:
            return
        self.filename_current = self.filenames[idx_cur]
        self.load_image()

    def load_image(self):
        img_path = os.path.join(self.file_dir, self.filename_current)
        self.central_window.change_src(img_path)

    def load_file(self, filename):
        # --Update file_list start-- #
        self.filename_current = filename.split('/')[-1]
        self.file_dir = os.path.dirname(filename)
        self.filenames = []
        self.file_list.clear()
        files = os.listdir(self.file_dir)
        for f in files:
            if '.' + f.split('.')[-1] in self.file_filters:
                self.filenames.append(f)
        self.filenames.sort()
        self.file_list.addItems(self.filenames)
        self.file_list.setCurrentRow(self.filenames.index(self.filename_current))
        # --Update file_list start-- #
        self.load_image()