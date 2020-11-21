import cv2 as cv
import numpy as np

img = cv.imread('test.jpg', 0)  # 读取图片，获取像素
print(np.shape(img))

data = np.array(img)
print(data.flatten())  # 转换成一维