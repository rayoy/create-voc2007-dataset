# -*- coding:utf-8 -*-

import cv2 as cv
import numpy as np
import random
from libs.shape import Shape, Point
from libs.pascal_voc_io import PascalVocWriter
from libs.pascal_voc_io import XML_EXT
from libs.labelFile import LabelFile
from PIL import Image, ImageDraw, ImageFont
import os.path

IMAGE_EXT = '.jpg'
FONT = ImageFont.truetype('fonts/simhei.ttf', 60)

# 定义添加高斯噪声的函数
def addGaussianNoise(image, percetage):
    G_Noiseimg = image
    G_NoiseNum = int(percetage * image.shape[0] * image.shape[1])
    for i in range(G_NoiseNum):
        temp_x = np.random.randint(20, 40)
        temp_y = np.random.randint(20, 40)
        G_Noiseimg[temp_x][temp_y] = 255
    return G_Noiseimg


# 定义添加椒盐噪声的函数
def SaltAndPepper(src, percetage):
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


def randomTable(num):
    # Create a black image
    img = np.zeros((512, 512, 3), np.uint8)
    img.fill(255)
    black = (0, 0, 0)
    left = random.randint(20, 100)
    top = random.randint(50, 200)
    width = random.randint(30, 100)
    height = random.randint(30, 100)

    row = random.randint(1, 3)
    column = random.randint(1, 3)

    rectShapes = []

    print("image:{}, row num={}, column num ={} ".format(num, row, column))

    draw = ImageDraw.Draw(img)
    for r in range(0, row):
        for c in range(0, column):
            left = left + c * width
            top = top + r * height
            start_point = (left + c * width, top + r * height)
            end_point = (left + (c + 1) * width, top + (r + 1) * height)

            # 画框
            cv.rectangle(img, start_point, end_point, black, 1)
            # 填字
            draw.text((left, top), u'大胃王狂欢', (255, 255, 0), font=FONT)

            points = [start_point, end_point]
            shape = Shape(label='rect')
            for x, y in points:
                shape.addPoint(Point(x, y))
            shape.close()
            rectShapes.append(shape)
    # font = cv.FONT_HERSHEY_SIMPLEX
    # cv.putText(img, 'Hello', (10, 500), font, 4, black, 1)
    imagePath = 'VOC2007/JPEGImages/'
    xmlPath = 'VOC2007/Annotations/'
    fileName = imagePath + num + IMAGE_EXT
    xmlName = xmlPath + num + XML_EXT
    print('fileName=', fileName)

    noise_percetage = random.uniform(0, .3)
    print('noise_percetage=', noise_percetage)

    SaltAndPepper_noiseImage = SaltAndPepper(img, 0)  # 添加10%的椒盐噪声

    cv.imwrite(fileName, SaltAndPepper_noiseImage)

    savePascalVocFormat(xmlName, rectShapes, imagePath, img)


#    cv.imshow("test", img)
#    cv.waitKey(0)
#    cv.destroyAllWindows()

def savePascalVocFormat(filename, shapes, imagePath, image):
    imgFolderPath = os.path.dirname(imagePath)
    imgFolderName = os.path.split(imgFolderPath)[-1]
    imgFileName = os.path.basename(imagePath)
    # imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]
    # Read from file path because self.imageData might be empty if saving to
    # Pascal format

    print(image.ctypes)
    print(image.shape)
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


# for i in range(4, 10000):
#    randomTable("%06d" % i)
randomTable("000000noise")

# srcImage = cv.imread("VOC2007/JPEGImages/000002.jpg")
# cv.namedWindow("Original image")
# cv.imshow("Original image", srcImage)
#
# gauss_noiseImage = addGaussianNoise(srcImage, 0.3)  # 添加10%的高斯噪声
# cv.imshow("Add_GaussianNoise Image", gauss_noiseImage)
# cv.imwrite("Glena.jpg ", gauss_noiseImage)
#
# SaltAndPepper_noiseImage = SaltAndPepper(srcImage, 0.1)  # 再添加10%的椒盐噪声
# cv.imshow("Add_SaltAndPepperNoise Image", SaltAndPepper_noiseImage)
#
# cv.waitKey(0)
# cv.destroyAllWindows()
