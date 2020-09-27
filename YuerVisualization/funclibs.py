import os
import cv2
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage, QPixmap

def new_icon(icon):
    icon_path = os.path.join(os.getcwd(), "icons/" + icon +".png")
    return QIcon(icon_path)

def cvimg_to_pixmap(cv2_imgbgr):
    cv2_imgrgb = cv2.cvtColor(cv2_imgbgr, cv2.COLOR_BGR2RGB)
    height, width, _ = cv2_imgrgb.shape
    bytes_per_line = 3 * width
    qtimg = QImage(cv2_imgrgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qtimg)
    return pixmap

def cvimgpath_to_qtpixmap(img_path):
    img_bgr = cv2.imread(img_path)
    pixmap = cvimg_to_pixmap(img_bgr)
    return pixmap

def get_videopath(img_path):
    img_dir = os.path.dirname(img_path)
    video_dir = os.path.join(img_dir, 'result_videos')
    img_file_name = img_path.split('/')[-1]
    img_name = img_file_name.split('.')[0]
    video_name = img_name + '.avi'
    video_path = os.path.join(video_dir, video_name)
    return video_path

class Video(object):
    def __init__(self):
        self.video_capture = cv2.VideoCapture()
        self.video_path = None
        self.frame_rate = 1
        self.frame_total_num = 0
        self.frame_current = 0  # the value represents that video capture read next
        self.frame_interval = 1
        self.video_height = 0
        self.video_width = 0
        self.pixmap_current = None

    def calculate_current_frame(self):
        pass

    def get_pixmap(self):
        flag, img_bgr = self.video_capture.read()
        if flag:
            self.pixmap_current = cvimg_to_pixmap(img_bgr)
            return True
        else:
            return False  # keep the canvas
    def get_video_info(self):
        self.frame_rate = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.frame_total_num = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    def video_open(self, video_path):
        self.video_path = video_path
        self.video_capture.open(video_path)
        if not self.video_capture.isOpened():
            return False
        else:
            flag = self.video_refresh()
            return flag

    def video_refresh(self):
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_current)
        flag = self.get_pixmap()
        if flag:
            self.get_video_info()
            return True
        else:
            return False

