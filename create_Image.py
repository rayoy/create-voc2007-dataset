# -*- coding:utf-8 -*-

import cv2 as cv
import numpy as np
import random
from libs.shape import Shape, Point
from libs.pascal_voc_io import PascalVocWriter
from libs.pascal_voc_io import XML_EXT
from libs.labelFile import LabelFile
import os.path

IMAGE_EXT = '.jpg'


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
    for r in range(0, row):
        for c in range(0, column):
            start_point = (left + c * width, top + r * height)
            end_point = (left + (c + 1) * width, top + (r + 1) * height)
            cv.rectangle(img, start_point, end_point,
                         black, 2)
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
    cv.imwrite(fileName, img)

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


for i in range(4, 10000):
    randomTable("%06d" % i)
