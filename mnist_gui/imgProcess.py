import cv2
import numpy as np


def ifSeed(x, y):
    """ 种子判断函数 """
    if x < 0 or x >= m or y < 0 or y >= n:
        return False
    if img3[x][y] == 0 and seedFlag[x][y] == 0:
        return True
    return False


def regionGrow():
    """ 区域生长 """
    res = []
    seeds = []
    for i in range(n - 1):
        for j in range(m - 1):
            if ifSeed(j, i):
                seeds.append([j, i])
                BFS(seeds, res)
    return res


def BFS(seeds, record):
    """
    广度优先搜索寻找各数字
    使用队列，列表头为队首
    """
    x_way, y_way = [-1, 0, 1, 0], [0, -1, 0, 1]
    min_x, max_x = seeds[0][0], seeds[0][0]
    min_y, max_y = seeds[0][1], seeds[0][1]
    flag = 0  # 用于排除噪声
    while len(seeds) > 0:
        currentSeed = seeds.pop(0)
        for i in range(4):
            temX = currentSeed[0] + x_way[i]
            temY = currentSeed[1] + y_way[i]
            if ifSeed(temX, temY):
                seeds.append([temX, temY])
                seedFlag[temX][temY] = 1
                flag += 1
                if temX < min_x:
                    min_x = temX
                if temX > max_x:
                    max_x = temX
                if temY < min_y:
                    min_y = temY
                if temY > max_y:
                    max_y = temY
    if flag > 100:
        record.append([min_x, min_y, max_x, max_y])


def process(image):
    """
    原始图像处理函数
    :param image: 原始图像文件
    :return: 输入模型的格式
    """
    # rgb转为灰度图
    img1 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # 获取图像长宽
    global m, n
    m, n = img1.shape

    # 定义标记数组，用于记录遍历情况
    global seedFlag
    seedFlag = np.zeros([m, n])

    # 图像二值化
    th, img2 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 进行膨胀处理避免不连通情况出现
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    global img3
    img3 = cv2.erode(img2, kernel)

    # 进行深度优先搜索找出各个数字的坐标
    division = regionGrow()

    output = []
    for i in division:
        # 截取各数字图像
        tem = img3[i[0]: i[2], i[1]: i[3]]
        edgeLenX = int((i[2] - i[0]) / 5)
        edgeLenY = int(((i[2] - i[0]) * 7 / 5 - (i[3] - i[1])) / 2)
        tem = cv2.copyMakeBorder(tem, edgeLenX, edgeLenX, edgeLenY, edgeLenY, cv2.BORDER_CONSTANT, value=255)

        # 进行相关处理使其能够输入模型
        tem = 255 - tem
        tem = cv2.resize(tem, (28, 28))
        tem = np.reshape(tem, (28, 28, 1))
        tem = tem / 255.0
        output.append(tem)

    output = np.array(output)
    return output
