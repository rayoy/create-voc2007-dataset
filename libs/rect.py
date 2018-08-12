#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
from libs.shape import Point


def drawDashRect(img, linelength, dashlength, start_point, end_point, color, thickness):
    w = end_point.x - start_point.x  # width
    h = end_point.y - start_point.y  # height

    totallength = int(dashlength + linelength)

    nCountX = int(w / totallength)
    nCountY = int(h / totallength)

    start = end_point
    end = end_point

    for i in (0, nCountY):
        end.x = start_point.x + (i + 1) * totallength - dashlength  # draw top dash line
        end.y = start_point.y
        start.x = start_point.x + i * totallength
        start.y = start_point.y
        cv.line(img, (start.x, start.y), (end.x, end.y), color,8, thickness)

    for i in (0, nCountY):
        start.x = start_point.x + i * totallength
        start.y = start_point.y + h
        end.x = start_point.x + (i + 1) * totallength - dashlength  # draw bottom dash line
        end.y = start_point.y + h
        cv.line(img, (start.x, start.y), (end.x, end.y), color, 8,thickness)

    for i in (0, nCountY):
        start.x = start_point.x
        start.y = start_point.y + i * totallength
        end.y = start_point.y + (i + 1) * totallength - dashlength  # draw left dash line
        end.x = start_point.x
        cv.line(img, (start.x, start.y), (end.x, end.y), color,8, thickness)

    for i in (0, nCountY):
        start.x = start_point.x + w
        start.y = start_point.y + i * totallength
        end.y = start_point.y + (i + 1) * totallength - dashlength  # draw right dash line
        end.x = start_point.x + w
        cv.line(img, (start.x, start.y), (end.x, end.y), color,8, thickness)


# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
img.fill(255)
start_point = Point(10, 10)
end_point = Point(200, 300)
cv.line(img, (1, 3), (50, 80), (0,0,0), 1)
#cv.rectangle(img, (start_point.x, start_point.y), (end_point.x, end_point.y), (0,0,0),8, 1)
drawDashRect(img, 1, 2, start_point, end_point, (0, 0, 0), 1)
winname = 'example'
cv.namedWindow(winname, 0)
cv.imshow(winname, img)
cv.waitKey(0)
