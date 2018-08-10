# -*- coding:utf-8 -*-

import cv2 as cv
import numpy as np
import random
import threading
from libs.shape import Shape, Point
from libs.pascal_voc_io import PascalVocWriter
from libs.pascal_voc_io import XML_EXT
from libs.labelFile import LabelFile
from PIL import Image, ImageDraw, ImageFont
import os.path

IMAGE_EXT = '.jpg'
BLACK = (0, 0, 0)
TEXT = ['当', '前', '逾', '期', '数', '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋',
        '沈', '韩', '杨', '贷', '款', '记', '录',
        '朱', '秦', '未', '还', '本', '金', '数',
        '尤', '许', '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴',
        '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '的', '一', '是', '了', '我', '不',
        '人', '在', '他',
        '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为', '子', '中', '你', '说', '生', '国', '年',
        '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以', '乾', '坤', 'A', 'I', 'P',
        "E"]


# 定义添加高斯噪声的函数
def addGaussianNoise(image):
    image.flags.writeable = True
    kernel_size = (5, 5)
    sigma = 1.5
    img = cv.GaussianBlur(image, kernel_size, sigma)
    return img


# 定义添加椒盐噪声的函数
def SaltAndPepper(src, percetage):
    src.flags.writeable = True
    SP_NoiseImg = src
    SP_NoiseNum = int(percetage * src.shape[0] * src.shape[1])
    for i in range(SP_NoiseNum):
        randX = random.randint(0, src.shape[0] - 1)
        randY = random.randint(0, src.shape[1] - 1)
        if random.randint(0, 1) == 0:
            SP_NoiseImg[randX, randY] = 0
        else:
            SP_NoiseImg[randX, randY] = 255
    return SP_NoiseImg


# 返回length的随机字符串（包含字间距），word_height 为字符串高度
def randomText(word_count):
    text = []
    for word in range(0, word_count):
        text.append(random.choice(TEXT))

    return ''.join(text)


def randomTable(num):
    # Create a black image
    img = np.zeros((512, 512, 3), np.uint8)
    img.fill(255)
    left = random.randint(20, 50)
    top = random.randint(50, 50)
    width = random.randint(100, 150)
    height = random.randint(30, 70)

    row = random.randint(2, 4)
    column = random.randint(2, 3)

    if row == 1 and column == 1:
        width, height = width * 2, height * 2

    rectShapes = []

    # print("image:{}, row num={}, column num ={} ".format(num, row, column))

    for r in range(0, row):
        if r % 2 == 0:
            cell_width = column * width
            start_point = (left, top + r * height)
            text_start_point = (
                start_point[0] + int(width * 0.1), start_point[1] + int(height * 0.1))
            end_point = (left + cell_width, top + (r + 1) * height)

            # PIL image转换成array
            img = Image.fromarray(np.uint8(img))
            draw = ImageDraw.Draw(img)
            word_height = int(height * 0.6)
            FONT = ImageFont.truetype('fonts/simhei.ttf', word_height)
            # 填字
            draw.text(text_start_point, randomText(int(cell_width / word_height - 1)), BLACK, font=FONT)
            # array转换成image
            img = np.asarray(img)
            # 画框
            thickness = [1, 2]  # 表格线粗细随机
            # cv.rectangle(img, start_point, end_point, BLACK, random.choice(thickness))

            # 用线画矩形
            top_right_point = (end_point[0], start_point[1])
            bottom_left_point = (start_point[0], end_point[1])
            cv.line(img, start_point, top_right_point, BLACK, 1)  # draw top line
            cv.line(img, bottom_left_point, end_point, BLACK, 1)  # draw bottom line
            #cv.line(img, start_point, bottom_left_point, BLACK, 1)  # draw left line
            #cv.line(img, top_right_point, end_point, BLACK, 1)  # draw right line

            points = [start_point, end_point]
            shape = Shape(label='rect')
            for x, y in points:
                shape.addPoint(Point(x, y))
            shape.close()
            rectShapes.append(shape)
            continue
        for c in range(0, column):
            start_point = (left + c * width, top + r * height)
            text_start_point = (
                start_point[0] + int(width * 0.1), start_point[1] + int(height * 0.1))
            end_point = (left + (c + 1) * width, top + (r + 1) * height)

            # PIL image转换成array
            img = Image.fromarray(np.uint8(img))
            draw = ImageDraw.Draw(img)
            word_height = int(height * 0.6)
            FONT = ImageFont.truetype('fonts/simhei.ttf', word_height)
            # 填字
            draw.text(text_start_point, randomText(int(width / word_height - 1)), BLACK, font=FONT)
            # array转换成image
            img = np.asarray(img)
            # 画框
            thickness = [1, 2]  # 表格线粗细随机
            # cv.rectangle(img, start_point, end_point, BLACK, random.choice(thickness))

            # 用线画矩形
            top_right_point = (end_point[0], start_point[1])
            bottom_left_point = (start_point[0], end_point[1])
            cv.line(img, start_point, top_right_point, BLACK, 1)  # draw top line
            cv.line(img, bottom_left_point, end_point, BLACK, 1)  # draw bottom line

            if c != 0:
                cv.line(img, start_point, bottom_left_point, BLACK, 1)  # draw left line
            if c != column - 1:
                cv.line(img, top_right_point, end_point, BLACK, 1)  # draw right line

            points = [start_point, end_point]
            shape = Shape(label='rect')
            for x, y in points:
                shape.addPoint(Point(x, y))
            shape.close()
            rectShapes.append(shape)

    # cv.namedWindow(num, 0)
    # cv.imshow(num, img)
    # cv.waitKey(0)

    imagePath = 'VOC2007/JPEGImages/'
    xmlPath = 'VOC2007/Annotations/'
    fileName = imagePath + num + IMAGE_EXT
    xmlName = xmlPath + num + XML_EXT
    # print('fileName=', fileName)

    noise_percetage = random.uniform(0, .25)
    #print('noise_percetage=', noise_percetage)

    salt_noise_image = SaltAndPepper(img, noise_percetage)  # 添加的椒盐噪声

    gaussian_noise_image = addGaussianNoise(salt_noise_image)  # 添加的高斯噪声

    cv.imwrite(fileName, gaussian_noise_image)

    savePascalVocFormat(xmlName, rectShapes, imagePath, img)


def savePascalVocFormat(filename, shapes, imagePath, image):
    imgFolderPath = os.path.dirname(imagePath)
    imgFolderName = os.path.split(imgFolderPath)[-1]
    imgFileName = os.path.basename(imagePath)
    # imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]
    # Read from file path because self.imageData might be empty if saving to
    # Pascal format

    imageShape = [image.shape[0], image.shape[1], image.shape[2]]
    writer = PascalVocWriter(imgFolderName, imgFileName,
                             imageShape, localImgPath=imagePath)

    def format_shape(s):
        return dict(label=s.label,
                    line_color=None,
                    fill_color=None,
                    points=[(p.x, p.y) for p in s.points],
                    # add chris
                    difficult=s.difficult)

    for shape in shapes:
        shape = format_shape(shape)
        points = shape['points']
        label = shape['label']
        # Add Chris
        difficult = int(shape['difficult'])
        bndbox = LabelFile.convertPoints2BndBox(points)
        writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3], label, difficult)

    writer.save(targetFile=filename)
    return


# for i in range(10, 20001):
#     randomTable("%06d" % i)
# 半封闭 + 合并单元格
#randomTable("000001")
#
# class generateImageThread(threading.Thread):
#     def __init__(self, name,s,e):
#         threading.Thread.__init__(self)
#         self.name = name
#         self.s = s
#         self.e = e
#
#     def run(self):
#         print("开始线程：{},{}-{}".format(self.name, self.s, self.e))
#         for index in range(self.s, self.e):
#             num = "%06d" % index
#             print(num)
#             randomTable(num)
#         print("退出线程：{},{}-{}".format(self.name, self.s, self.e))
#
#
# # 多线程
# for step in range(24001, 26000, 50):
#     thread = generateImageThread(step, step, step + 50)
#     # 开启新线程
#     thread.start()


# 删除掉 生成的图片
print('delete image 024001.jpg ~ 026000.jpg')
for index in range(24001, 26000):
    num = "%06d" % index
    imagePath = 'VOC2007/JPEGImages/'
    xmlPath = 'VOC2007/Annotations/'
    fileName = imagePath + num + IMAGE_EXT
    xmlName = xmlPath + num + XML_EXT
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print('no such file:', fileName)

    if os.path.exists(xmlName):
        os.remove(xmlName)
    else:
        print('no such file:', xmlName)
