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


def randomTable(num):
    # Create a black image
    img = np.zeros((512, 512, 3), np.uint8)
    img.fill(255)
    left = random.randint(20, 50)
    top = random.randint(30, 50)
    width = random.randint(100, 150)
    height = random.randint(30, 70)

    row = random.randint(2, 4)
    column = random.randint(2, 3)

    if row == 1 and column == 1:
        width, height = width * 2, height * 2

    rectShapes = []

    # print("image:{}, row num={}, column num ={} ".format(num, row, column))

    for r in range(0, row):
        for c in range(0, column):
            start_point = (left + c * width, top + r * height)
            end_point = (left + (c + 1) * width, top + (r + 1) * height)

            # 画框
            thickness = [1, 2]  # 表格线粗细随机
            cv.rectangle(img, start_point, end_point, BLACK, random.choice(thickness))

            points = [start_point, end_point]
            shape = Shape(label='rect')
            for x, y in points:
                shape.addPoint(Point(x, y))
            shape.close()
            rectShapes.append(shape)

    imagePath = 'VOC2007/JPEGImages/'
    xmlPath = 'VOC2007/Annotations/'
    fileName = imagePath + num + IMAGE_EXT
    xmlName = xmlPath + num + XML_EXT
    # print('fileName=', fileName)

    cv.imwrite(fileName, img)

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
#randomTable("000001")
#
class generateImageThread(threading.Thread):
    def __init__(self, name,s,e):
        threading.Thread.__init__(self)
        self.name = name
        self.s = s
        self.e = e

    def run(self):
        print("开始线程：{},{}-{}".format(self.name, self.s, self.e))
        for index in range(self.s, self.e):
            num = "%06d" % index
            print(num)
            randomTable(num)
        print("退出线程：{},{}-{}".format(self.name, self.s, self.e))


# 多线程
for step in range(40001, 42000, 50):
    thread = generateImageThread(step, step, step + 50)
    # 开启新线程
    thread.start()
