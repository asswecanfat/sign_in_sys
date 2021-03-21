import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def get_KNN(people_num: int, face: np.ndarray, label: np.ndarray):
    """
    将数据放入knn分类器训练

    :param people_num: 总人数
    :param face: 面部数据
    :param label: 标签数据
    :return:
    """
    np.random.seed(0)
    knn = KNeighborsClassifier(people_num)  # 定义一个knn分类器对象
    knn.fit(face, label)
    return knn
