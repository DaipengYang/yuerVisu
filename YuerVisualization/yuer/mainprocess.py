import cv2
import os
import numpy as np
from yuer.input0 import iter

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

    img_path = os.path.join(img_dir, "1.jpeg")
    img = cv2.imread(img_path)
    video_path = os.path.join(videos_dir, '1.avi')
    fps = 5
    img_shape = img.shape
    size = (img_shape[1], img_shape[0])
    fourcc = cv2.VideoWriter_fourcc('M','P','E','G')
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, size)
    if not video_writer.isOpened():
        print("writer is not opened!")
    labels_path = os.path.join(img_dir, 'labels.txt')
    f = open(labels_path, 'w')
    # src
    video_writer.write(img)
    f.write('src'+'\n')
    # gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_saved = np.dstack([gray, gray, gray])
    video_writer.write(gray_saved)
    f.write('gray'+'\n')
    # retina_avg
    input = gray
    for i in range(1, 6):
        input = iter(input, i)
        result = np.dstack([input, input, input])
        result_saved = result.astype(np.uint8)
        video_writer.write(result_saved)
        label = "retina_avg_" + str(i) + '\n'
        f.write(label)
        print("This is {} th iteration".format(i))


    video_writer.release()
    f.close()

if __name__ == "__main__":
    test()