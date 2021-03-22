from pathlib import Path

import joblib
import cv2
import numpy as np

model_file = Path(__file__).parent.parent / Path('data_file/stu_face.model')


def _init_mod():
    """
    训练好的模型载入
    """
    try:
        mod, data_mean, r_num_vector = joblib.load(model_file)
    except FileNotFoundError:
        return None
    return mod, data_mean, r_num_vector


class Mod_User:
    def __init__(self):
        self.mod, self.data_mean, self.r_num_vector = _init_mod()

    def recognize(self, face, label):
        img = cv2.resize(np.asarray(bytearray(face), dtype="uint8"), (100, 100), )  # 读取图片并重设大小
        rows, cols = img.shape
        recognize_face = np.zeros((1, 100 * 100))
        recognize_face[0, :] = np.reshape(img, (1, rows * cols))
        num_test = recognize_face.shape[0]
        temp_face = recognize_face - np.tile(self.data_mean, (num_test, 1))
        data_test_new = np.array(temp_face * self.r_num_vector)
        return int(self.mod.predict(data_test_new)[0]) == label


if __name__ == '__main__':
    m = Mod_User()
