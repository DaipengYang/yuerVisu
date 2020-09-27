import cv2
import os
import numpy as np

def avg_mat_3x3(npmat):
    shape = npmat.shape
    height = shape[0]
    width = shape[1]
    npmat = npmat.astype(np.float32)
    npmat_pad = np.pad(npmat, ((1, 1), (1, 1)), mode="edge")
    result = np.zeros((height, width), dtype=np.float32)
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            lt = npmat_pad[i, j] + 1.0 / np.sqrt(2) * (npmat_pad[i-1, j-1] - npmat_pad[i, j])
            rt = npmat_pad[i, j] + 1.0 / np.sqrt(2) * (npmat_pad[i-1, j+1] - npmat_pad[i, j])
            lb = npmat_pad[i, j] + 1.0 / np.sqrt(2) * (npmat_pad[i+1, j-1] - npmat_pad[i, j])
            rb = npmat_pad[i, j] + 1.0 / np.sqrt(2) * (npmat_pad[i+1, j+1] - npmat_pad[i, j])
            value = 0.5 * npmat_pad[i, j] \
                    + 0.0625 * npmat_pad[i-1, j] + 0.0625 * npmat_pad[i, j-1] \
                    + 0.0625 * npmat_pad[i, j+1] + 0.0625 * npmat_pad[i+1, j] \
                    + 0.0625 * lt + 0.0625 * rt + 0.0625 * lb + 0.0625 * rb
            # value = 0.125 * npmat_pad[i - 1, j] + 0.125 * npmat_pad[i, j - 1] \
            #         + 0.125 * npmat_pad[i, j + 1] + 0.125 * npmat_pad[i + 1, j] \
            #         + 0.125 * lt + 0.125 * rt + 0.125 * lb + 0.125 * rb
            result[i-1, j-1] = value
    return result


def get_avg_illu_retina(img_gray):
    avg_illu_retina = avg_mat_3x3(img_gray)
    return avg_illu_retina

def iter(img_gray, nums):
    result = img_gray
    for i in range(nums):
        result = get_avg_illu_retina(result)
    return result

def test():
    cwd = os.getcwd()
    img_dir = os.path.join(os.path.dirname(cwd), 'testpics')
    img_path = os.path.join(img_dir, "7.png")
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    avg_illu = iter(img_gray, 1)
    avg_illu.astype(np.uint8)
    cv2.imwrite(os.path.join(img_dir, 'gray.png'), img_gray)
    cv2.imwrite(os.path.join(img_dir, 'result.png'), avg_illu)

if __name__ == "__main__":
    test()