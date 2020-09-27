import cv2
import os
import numpy as np

def mkdir_y(dirname):
    """ Create directory recurrently if it is not being, else do nothing. """
    if not os.path.exists(dirname):
        mkdir_y(os.path.dirname(dirname))
        os.mkdir(dirname)
    return dirname

def test():
    cwd = os.getcwd()
    proj_dir = os.path.dirname(cwd)
    img_dir = os.path.join(proj_dir, "testpics")
    videos_dir = mkdir_y(os.path.join(img_dir, "result_videos"))

    img_path = os.path.join(img_dir, "7.png")
    img = cv2.imread(img_path)
    video_path = os.path.join(videos_dir, '7.avi')
    fps = 5
    img_shape = img.shape
    size = (img_shape[1], img_shape[0])
    fourcc = cv2.VideoWriter_fourcc('M','P','E','G')
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, size)
    if not video_writer.isOpened():
        print("writer is not opened!")
    for i in range(100):
        if i % 5 == 0:
            video_writer.write(img)
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mat = np.zeros((size[1], size[0], 3), dtype=np.uint8)
            mat[:, :, 0] = gray
            mat[:, :, 1] = gray
            mat[:, :, 2] = gray
            video_writer.write(mat)
    video_writer.release()

if __name__ == "__main__":
    test()