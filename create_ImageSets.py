# -*- coding:utf-8 -*-

import os

__author__ = 'peic'

'''
设置trainval和test数据集包含的图片
'''

# ImageSets文件夹
_IMAGE_SETS_PATH = 'VOC2007/ImageSets'
_MAin_PATH = 'VOC2007/ImageSets/Main'
_XML_FILE_PATH = 'VOC2007/Annotations'

# Train数据集编号
_TRAIN_NUMBER = 2895

if __name__ == '__main__':

    # 创建ImageSets数据集
    if os.path.exists(_IMAGE_SETS_PATH):
        print('ImageSets dir is already exists')
        if os.path.exists(_MAin_PATH):
            print('Main dir is already in ImageSets')
    else:
        os.mkdir(_IMAGE_SETS_PATH)
        os.mkdir(_MAin_PATH)

    f_test = open(os.path.join(_MAin_PATH, 'test.txt'), 'w')
    f_train = open(os.path.join(_MAin_PATH, 'trainval.txt'), 'w')

    # 遍历XML文件夹
    for root, dirs, files in os.walk(_XML_FILE_PATH):
        print(len(files))
        for f in files:
            i = int(f.split('.')[0])
            if 1 < i < 400 or \
                    2001 < i < 2400 or \
                    20001 < i < 20400 or \
                    22001 < i < 22400 or \
                    24001 < i < 24400 or \
                    26001 < i < 26400 or \
                    28001 < i < 28400 or \
                    30001 < i < 30400 or \
                    32001 < i < 32400 or \
                    34001 < i < 34400 or \
                    36001 < i < 36400 or \
                    38001 < i < 38400 or \
                    40001 < i < 40400:
                f_test.write(f.split('.')[0] + '\n')
            else:
                f_train.write(f.split('.')[0] + '\n')

            i += 1

    f_test.close()
    f_train.close()
