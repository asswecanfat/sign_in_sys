import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
from pathlib import Path

REAL_DISTANCE = 4
file_path = [i for i in Path(__file__).parent.iterdir() if i.is_dir()]


def img2vector(image):
    """
    读取图片并转换为一维向量

    :param image:图片
    :return:一维向量
    """
    print(image)
    img = cv2.resize(cv2.imread(image, 0), (100, 100), )  # 读取图片并重设大小
    rows, cols = img.shape  # 获取图片的像素
    # img_vector = np.zeros((1, rows * cols))  # 初始值均设置为0，大小就是图片像素的大小
    img_vector = np.reshape(img, (1, rows * cols))  # 使用imgVector变量作为一个向量存储图片矢量化信息
    return img_vector


def load_img(img_num: int, people_num: int):
    """
    加载图片集，可分为训练集和测试集

    :param img_num: 选择每个人img_num张图片
    :param people_num: 人数
    :return: 一维向量集合和对应的标签
    """
    face = np.zeros((people_num * img_num, 100 * 100))
    label = np.zeros(people_num * img_num)  # [0,0,.....0](共40*k个0)
    sample = np.random.permutation(img_num) + 1  # 随机排序1-10 (0-9）+1
    for num, i in enumerate(file_path):  # 共有people_num个人
        for j in range(img_num):  # 每个人都有10张照片
            image = str(i / Path(f'{sample[j]}.jpg'))
            # 读取图片并进行矢量化,构成训练集
            face[num * img_num + j, :] = img2vector(image)
            label[num * img_num + j] = num + 1
    return face, label


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
    r_num_vector = d_value.T * characteristic_vector[:, 0:vector_num]  # 按列取前r个特征向量,小矩阵特征向量向大矩阵特征向量过渡
    for i in range(vector_num):
        r_num_vector[:, i] = r_num_vector[:, i] / np.linalg.norm(r_num_vector[:, i])  # 特征向量归一化
    final_face_data = d_value * r_num_vector
    return final_face_data, face_mean, r_num_vector


# def face_recongize_old(image) -> str:
#     train_face, train_label = load_img(5, 3)
#     test_face = np.zeros((1, 100 * 100))
#     img = cv2.resize(image, (100, 100), )
#     rows, cols = img.shape  # 获取图片的像素
#     test_face[0, :] = np.reshape(img, (1, rows * cols))
#     # 将图片降维到10维
#     data_train_new, data_mean, V_r = pca(train_face, 10)
#     num_train = data_train_new.shape[0]  # 训练脸总数
#     num_test = test_face.shape[0]  # 测试脸总数
#     temp_face = test_face - np.tile(data_mean, (num_test, 1))
#     data_test_new = np.array(temp_face * V_r)  # 得到测试脸在特征向量下的数据,mat change to array
#     data_train_new = np.array(data_train_new)
#
#     for i in range(num_test):
#         test_f = data_test_new[i, :]
#         diff_mat = data_train_new - np.tile(test_f, (num_train, 1))  # 训练数据与测试脸之间距离
#         sq_diff_mat = diff_mat ** 2
#         sq_distances = sq_diff_mat.sum(axis=1)  # 按行求和
#         sorted_dist_indicies = sq_distances.argsort()  # 对向量从小到大排序，使用的是索引值,得到一个向量
#         index_min = sorted_dist_indicies[0]  # 距离最近的索引
#         return str(train_label[index_min]) if index_min < REAL_DISTANCE else 'Unknown'


def face_recongize_knn(image) -> str:
    """
    一维面部数据向量处理

    :param image:面部帧
    :return: 预测值
    """
    train_face, train_label = load_img(10, 1)
    test_face = np.zeros((1, 100 * 100))
    img = cv2.resize(image, (100, 100), )
    rows, cols = img.shape  # 获取图片的像素
    test_face[0, :] = np.reshape(img, (1, rows * cols))
    test_label = np.zeros(1)
    test_label[0] = 1
    num_test = test_face.shape[0]
    data_train_new, data_mean, r_num_vector = pca(train_face, 10)
    temp_face = test_face - np.tile(data_mean, (num_test, 1))
    data_test_new = np.array(temp_face * r_num_vector)  # 得到测试脸在特征向量下的数据,mat change to array
    return knn_com(data_train_new, train_label, data_test_new)


def camera_face():
    """
    展示用

    :return: None
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        frame_detected = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        try:
            x, y, w, h = frame_detected[0]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pre = face_recongize_knn(gray[y:y + h, x:x + w])
            cv2.putText(frame, pre, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        except IndexError:
            pass
        finally:
            cv2.imshow('face_capture', frame)
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def knn_com(data, label, input_data) -> str:
    """
    knn聚类算法

    :param data: 一维面部数据向量
    :param label: 一维面部数据向量对应的一维标签向量
    :param input_data: 输入的一维面部数据向量
    :return: 预测标签字符串
    """
    np.random.seed(0)
    knn = KNeighborsClassifier()  # 定义一个knn分类器对象
    knn.fit(data, label)  # 调用该对象的训练方法，主要接收两个参数：训练数据集及其样本标签
    label_predict = knn.predict(input_data)
    print(knn.predict_proba(input_data))
    # probility = knn.predict_proba(test_data)
    # score = knn.score(test_data, test_label, sample_weight=None)
    # print(label_predict, probility, score)
    return str(label_predict[0])


if __name__ == '__main__':
    # face_recongize(r'1/7.jpg')
    camera_face()
    # img2vector(r'1/7.jpg')
    # img = cv2.imread('1/8.jpg', 0)  # 读取图片
