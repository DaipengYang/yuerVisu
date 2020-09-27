import cv2
import os
from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QSlider, QListWidget, QPushButton, QScrollArea
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import QTimer
from canvas import Canvas
from funclibs import new_icon, get_videopath, cvimg_to_pixmap, cvimgpath_to_qtpixmap, Video

class CentralWindow(QWidget):
    def __init__(self):
        super(CentralWindow, self).__init__()
        ##### --Layout start-- #####
        # --left-- #
        self.canvas_image = Canvas()
        self.scroll_area_image = QScrollArea()
        self.scroll_area_image.setWidget(self.canvas_image)
        self.scroll_area_image.setWidgetResizable(True)
        self.canvas_result = Canvas()
        self.scroll_area_result = QScrollArea()
        self.scroll_area_result.setWidget(self.canvas_result)
        self.scroll_area_result.setWidgetResizable(True)
        # --right-- #
        self.video_info_label = QLabel("Video info")
        self.image_size_label = QLabel("Frame size")
        self.image_size_value = QLabel("0 0")
        self.frame_rate_label = QLabel("Frame rate")
        self.frame_rate_value = QLabel("1")
        self.frame_total_label = QLabel("Frame total num")
        self.frame_total_value = QLabel("0")
        self.frame_current_label = QLabel("Frame current")
        self.frame_current_value = QSpinBox()
        self.frame_current_value.setMinimum(0)
        self.frame_current_value.setSingleStep(1)
        self.frame_current_value.setValue(0)
        self.frame_current_value.setMaximum(10000)
        self.frame_current_value.setEnabled(False)
        self.frame_interval_label = QLabel('Frame interval')
        self.frame_interval_value = QSpinBox()
        self.frame_interval_value.setMinimum(1)
        self.frame_interval_value.setSingleStep(1)
        self.frame_interval_value.setMaximum(128)
        self.frame_interval_value.setValue(1)
        self.frame_interval_value.setEnabled(False)
        self.zoom_rate_label = QLabel("Zoom(%)")
        self.zoom_rate_value = QSpinBox()
        self.zoom_rate_value.setMinimum(20)
        self.zoom_rate_value.setMaximum(300)
        self.zoom_rate_value.setValue(100)
        self.zoom_rate_value.setSingleStep(10)
        self.zoom_reset_button = QPushButton()
        self.zoom_reset_button.setText('Reset')
        self.zoom_reset_button.setFixedWidth(50)
        zoom_hbox_layout = QHBoxLayout()
        zoom_hbox_layout.addWidget(self.zoom_rate_label)
        zoom_hbox_layout.addWidget(self.zoom_rate_value)
        zoom_hbox_layout.addWidget(self.zoom_reset_button)
        zoom_container = QWidget()
        zoom_container.setLayout(zoom_hbox_layout)
        self.video_play_pause_button = QPushButton()
        self.video_play_pause_button.setCheckable(True)
        self.video_play_pause_button.setIcon(new_icon('play'))
        self.video_play_pause_button.setFixedWidth(50)
        self.video_play_pause_button.setEnabled(False)
        self.frame_next_button = QPushButton()
        self.frame_next_button.setIcon(new_icon('nextframe'))
        self.frame_next_button.setFixedWidth(40)
        self.frame_next_button.setEnabled(False)
        self.frame_prev_button = QPushButton()
        self.frame_prev_button.setIcon(new_icon('prevframe'))
        self.frame_prev_button.setFixedWidth(40)
        self.frame_prev_button.setEnabled(False)
        pause_hbox_layout = QHBoxLayout()
        pause_hbox_layout.addWidget(self.video_play_pause_button)
        pause_hbox_layout.addWidget(self.frame_prev_button)
        pause_hbox_layout.addWidget(self.frame_next_button)
        pause_hbox_container = QWidget()
        pause_hbox_container.setLayout(pause_hbox_layout)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.image_size_label, 0, 0)
        grid_layout.addWidget(self.image_size_value, 0, 1)
        grid_layout.addWidget(self.frame_rate_label, 1, 0)
        grid_layout.addWidget(self.frame_rate_value, 1, 1)
        grid_layout.addWidget(self.frame_total_label, 2, 0)
        grid_layout.addWidget(self.frame_total_value, 2, 1)
        grid_layout.addWidget(self.frame_current_label, 3, 0)
        grid_layout.addWidget(self.frame_current_value, 3, 1)
        grid_layout.addWidget(self.frame_interval_label, 4, 0)
        grid_layout.addWidget(self.frame_interval_value, 4, 1)
        grid_layout.addWidget(zoom_container, 5, 0, 1, 2)
        grid_layout.addWidget(pause_hbox_container, 6, 0, 1, 2)
        grid_container = QWidget()
        grid_container.setLayout(grid_layout)
        self.frame_labels_label = QLabel("Names list")
        self.frame_labels_list = QListWidget()
        right_vbox_layout = QVBoxLayout()
        right_vbox_layout.addWidget(self.video_info_label)
        right_vbox_layout.addWidget(grid_container)
        right_vbox_layout.addWidget(self.frame_labels_label)
        right_vbox_layout.addWidget(self.frame_labels_list)
        right_vbox_container = QWidget()
        right_vbox_container.setLayout(right_vbox_layout)
        right_vbox_container.setMaximumWidth(250)
        # --widget layout-- #
        widget_hbox_layout = QHBoxLayout()
        widget_hbox_layout.addWidget(self.scroll_area_image)
        widget_hbox_layout.addWidget(self.scroll_area_result)
        widget_hbox_layout.addWidget(right_vbox_container)
        self.setLayout(widget_hbox_layout)
        ##### --Layout end-- #####

        ##### --Widget slot start-- #####
        # --scroll bar -start--#
        self.vertical_scroll_bar_image = self.scroll_area_image.verticalScrollBar()
        self.horizontal_scroll_bar_image = self.scroll_area_image.horizontalScrollBar()
        self.vertical_scroll_bar_result = self.scroll_area_result.verticalScrollBar()
        self.horizontal_scroll_bar_result = self.scroll_area_result.horizontalScrollBar()
        self.vertical_scroll_bar_image.valueChanged.connect(self.scroll_bar_imgv_moved)
        self.horizontal_scroll_bar_image.valueChanged.connect(self.scroll_bar_imgh_moved)
        self.vertical_scroll_bar_result.valueChanged.connect(self.scroll_bar_resultv_moved)
        self.horizontal_scroll_bar_result.valueChanged.connect(self.scroll_bar_resulth_moved)
        # --scroll bar -end--#
        # --zoom -start--#
        self.zoom_reset_button.clicked.connect(self.zoom_rate_value_reset)
        self.zoom_rate_value.valueChanged.connect(self.zoom_rate_value_changed)
        # --zoom -end--#
        self.frame_labels_list.doubleClicked.connect(self.frame_labels_list_doubleclicked)
        self.frame_current_value.valueChanged.connect(self.frame_current_value_changed)
        self.frame_interval_value.valueChanged.connect(self.frame_interval_value_changed)
        self.video_play_pause_button.toggled.connect(self.video_play_pause_button_changed)
        self.frame_next_button.clicked.connect(self.frame_next_button_clicked)
        self.frame_prev_button.clicked.connect(self.frame_prev_button_clicked)
        ##### --Widget slot end-- #####

        ##### --Initial state start-- #####
        self.labels = []
        self.img_path = None
        self.pixmap = None
        self.video = Video()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_timeout)
        ##### --Initial state end-- #####

    def scroll_bar_imgv_moved(self):
        self.vertical_scroll_bar_result.setValue(self.vertical_scroll_bar_image.value())
    def scroll_bar_imgh_moved(self):
        self.horizontal_scroll_bar_result.setValue(self.horizontal_scroll_bar_image.value())
    def scroll_bar_resultv_moved(self):
        self.vertical_scroll_bar_image.setValue(self.vertical_scroll_bar_result.value())
    def scroll_bar_resulth_moved(self):
        self.horizontal_scroll_bar_image.setValue(self.horizontal_scroll_bar_result.value())

    def zoom_rate_value_reset(self):
        self.zoom_rate_value.setValue(100)
    def zoom_rate_value_changed(self, value):
        self.canvas_image.zoom_rate = value
        self.canvas_result.zoom_rate = value
        self.canvas_image.repaint()
        self.canvas_result.repaint()

    def frame_labels_list_doubleclicked(self):
        idx = self.frame_labels_list.currentRow()
        if self.frame_current_value == idx:
            return
        else:
            self.video.frame_current = idx
            self.frame_current_value.setValue(self.video.frame_current)

    def frame_current_value_changed(self):
        self.video.frame_current = self.frame_current_value.value()
        if self.video.frame_current > self.video.frame_total_num - 1:
            self.video.frame_current = self.video.frame_total_num - 1
            self.frame_current_value.setValue(self.video.frame_current)
        elif self.video.frame_current < 0:
            self.video.frame_current = 0
            self.frame_current_value.setValue(self.video.frame_current)
        else:
            self.repaint_video_canvas()

    def frame_interval_value_changed(self):
        self.video.frame_interval = self.frame_interval_value.value()

    def timer_timeout(self):
        self.video.frame_current += self.video.frame_interval
        self.frame_current_value.setValue(self.video.frame_current)

    def video_play_pause_button_changed(self):
        if self.video_play_pause_button.isChecked():
            self.timer.start(1000 / self.video.frame_rate)
            self.video_play_pause_button.setIcon(new_icon('pause'))
            self.controlpanelstatus_enabled_false()
        else:
            self.timer.stop()
            self.video_play_pause_button.setIcon(new_icon('play'))
            self.controlpanelstatus_enabled_true()

    def frame_next_button_clicked(self):
        self.video.frame_current += self.frame_interval_value.value()
        if self.video.frame_current > self.video.frame_total_num - 1:
            self.video.frame_current = self.video.frame_total_num
        self.frame_current_value.setValue(self.video.frame_current)

    def frame_prev_button_clicked(self):
        self.video.frame_current -= self.frame_interval_value.value()
        if self.video.frame_current < 0:
            self.video.frame_current = 0
        self.frame_current_value.setValue(self.video.frame_current)

    def update_controlpanel(self):
        self.image_size_value.setText((str(self.video.video_height)+' '+str(self.video.video_width)))
        self.frame_current_value.setValue(self.video.frame_current)
        self.frame_rate_value.setText(str(self.video.frame_rate))
        self.frame_interval_value.setValue(self.video.frame_interval)
        self.frame_total_value.setText(str(self.video.frame_total_num))
        self.canvas_result.load_pixmap(self.video.pixmap_current)
    def controlpanelstatus_enabled_true(self):
        self.frame_current_value.setEnabled(True)
        self.frame_interval_value.setEnabled(True)
        self.frame_next_button.setEnabled(True)
        self.frame_prev_button.setEnabled(True)
    def controlpanelstatus_enabled_false(self):
        self.frame_current_value.setEnabled(False)
        self.frame_interval_value.setEnabled(False)
        self.frame_next_button.setEnabled(False)
        self.frame_prev_button.setEnabled(False)
    def change_image(self, img_path):
        self.img_path = img_path
        if self.img_path is None:
            return
        self.pixmap = cvimgpath_to_qtpixmap(img_path)
        self.canvas_image.load_pixmap(self.pixmap)
    def change_video(self, video_path):
        if not os.path.exists(video_path):
            self.scroll_area_result.hide()
            self.video_play_pause_button.setEnabled(False)
            self.controlpanelstatus_enabled_false()
            return
        else:
            flag = self.video.video_open(video_path)
            if not flag:
                QMessageBox.critical(self, "Note", "The video does not open, please check your code or video!")
            else:
                self.update_controlpanel()
                self.video_play_pause_button.setEnabled(True)
                self.controlpanelstatus_enabled_true()
                self.scroll_area_result.show()
                self.change_labels_list(video_path)
    def change_labels_list(self, video_path):
        video_dir = os.path.dirname(video_path)
        img_dir = os.path.dirname(video_dir)
        file_path = os.path.join(img_dir, 'labels.txt')
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.labels.append(line.strip())
        for item in self.labels:
            self.frame_labels_list.addItem(item)
    def change_src(self, img_path):
        self.change_image(img_path)
        video_path = get_videopath(self.img_path)
        self.change_video(video_path)

    def repaint_video_canvas(self):
        flag = self.video.video_refresh()
        if flag:
            self.canvas_result.load_pixmap(self.video.pixmap_current)
        else:
            QMessageBox.critical(self, 'Error', "Please check your current frame!")
            self.scroll_area_result.hide()
