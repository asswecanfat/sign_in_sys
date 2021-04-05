from pathlib import Path
from typing import Tuple, List

import numpy as np
import cv2
import joblib

from knn_face import get_KNN, KNeighborsClassifier

data_file: List = [i for i in (Path(__file__).parent.parent / Path('data_file/stu_face')).iterdir()]
model_file_path = Path(__file__).parent.parent / Path('data_file')


def load_img(all_img_num: int,
             people_num: int) -> Tuple[np.ndarray,
                                       np.ndarray,
                                       np.ndarray,
                                       np.ndarray]:
    """
    加载图片集，可分为训练集和测试集

    :param all_img_num: 总共all_img_num张图片
    :param people_num: 人数
    :return: 一维向量集合和对应的标签的训练集和测试集
    """
    train_img_num = int(all_img_num * 0.8)  # 将总图片的80%的数量作为训练图片
    train_face = np.zeros((people_num * train_img_num, 100 * 100))
    train_label = np.zeros(people_num * train_img_num)  # [0,0,.....0](共40*k个0)
    test_face = np.zeros((people_num * (all_img_num - train_img_num),
                          100 * 100))
    test_label = np.zeros(people_num * (all_img_num - train_img_num))
    sample = np.random.permutation(all_img_num)  # 随机排序1-all_img_num (0-9）+1
    for num, pic_dir in enumerate(data_file):  # 共有people_num个人
        for j in range(all_img_num):  # 每个人都有10张照片
            image = str(pic_dir / Path(f'{sample[j]}.jpg'))
            temp = img2vector(image)
            # 读取图片并进行矢量化,构成训练集
            if j < train_img_num:
                train_x = num * train_img_num + j
                train_face[train_x, :] = temp
                train_label[train_x] = int(pic_dir.name)
            else:
                test_x = num * (all_img_num - train_img_num) + (j - train_img_num)
                test_face[test_x, :] = temp
                test_label[test_x] = int(pic_dir.name)
    return train_face, train_label, test_face, test_label


def img2vector(image: str):
    """
    读取图片并转换为一维向量

    :param image:图片路径
    :return:一维向量
    """
    img = cv2.resize(cv2.imread(image, 0), (100, 100), )  # 读取图片并重设大小
    rows, cols = img.shape  # 获取图片的像素
    # img_vector = np.zeros((1, rows * cols))  # 初始值均设置为0，大小就是图片像素的大小
    img_vector = np.reshape(img, (1, rows * cols))  # 使用imgVector变量作为一个向量存储图片矢量化信息
    return img_vector


def pca(face_data, vector_num: int):  # 参数r代表降低到r维
    """
    PCA算法

    :param face_data: 一维面部数据向量
    :param vector_num: 代表降低到vector_num维
    :return: 降维后的一维面部数据向量，平均脸向量和vector_num维向量
    """
    data = np.float32(np.mat(face_data))
    rows, cols = np.shape(data)
    face_mean = np.mean(data, 0)  # 对列求平均值
    d_value = data - np.tile(face_mean, (rows, 1))  # 将所有样例减去对应均值得到A
    covariance_matrix = d_value * d_value.T  # 得到协方差矩阵
    characteristic_value, characteristic_vector = np.linalg.eig(covariance_matrix)  # 求协方差矩阵的特征值和特征向量
    r_num_vector = d_value.T * characteristic_vector[:, :vector_num]  # 按列取前r个特征向量,小矩阵特征向量向大矩阵特征向量过渡
    for i in range(vector_num):
        r_num_vector[:, i] /= np.linalg.norm(r_num_vector[:, i])  # 特征向量归一化
    final_face_data = d_value * r_num_vector
    return final_face_data, face_mean, r_num_vector


def start_train():
    """
    使用knn算法进行训练并打包成模型

    """
    people_num = len(data_file)
    train_face, train_label, test_face, test_label = load_img(all_img_num=10, people_num=people_num)
    data_train_new, data_mean, r_num_vector = pca(face_data=train_face, vector_num=10)
    # num_train = data_train_new.shape[0]  # 训练脸总数
    num_test = test_face.shape[0]  # 测试脸总数
    temp_face = test_face - np.tile(data_mean, (num_test, 1))
    data_test_new = temp_face * r_num_vector  # 得到测试脸在特征向量下的数据
    data_test_new = np.array(data_test_new)  # mat change to array
    data_train_new = np.array(data_train_new)

    knn = get_KNN(people_num=people_num, face=data_train_new, label=train_label)
    model_test(knn, data_test_new)
    joblib.dump((knn, data_mean, r_num_vector),
                str(model_file_path / Path('stu_face.model')))


def model_test(model: KNeighborsClassifier, data_test: np.ndarray):
    for test_face in data_test:
        label_predict = model.predict_proba(np.array([test_face]))
        print(label_predict[0])


if __name__ == '__main__':
    # print(data_file.is_dir())
    # print(type(np.zeros((3,3))))
    # for num, i in enumerate(data_file.iterdir()):
    #     print(num, i.name)
    # print((data_file[0] / Path('1.jpg')).exists())
    start_train()
