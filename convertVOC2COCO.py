import os, sys, shutil
import xml.etree.ElementTree as ET
import xmltodict
import json
from xml.dom import minidom
from collections import OrderedDict


# attrDict = {"images":[{"file_name":[],"height":[], "width":[],"id":[]}], "type":"instances", "annotations":[], "categories":[]}

# xmlfile = "000023.xml"

def generateVOC2Json(rootDir, xmlFiles, tag):
    attrDict = dict()
    # images = dict()
    # images1 = list()
    attrDict["categories"] = [{"supercategory": "none", "id": 1, "name": "rect"}]
    images = list()
    annotations = list()
    for root, dirs, files in os.walk(rootDir):
        image_id = 0
        for file in xmlFiles:
            image_id = image_id + 1
            old_file_name = os.path.join('VOC2007/JPEGImages', file + '.jpg')
            coco_file_name = 'COCO_'+tag+'_'+file + '.jpg'
            new_file_name = os.path.join('COCO/'+tag, coco_file_name)
            # copy 文件

            shutil.copyfile(old_file_name, new_file_name)

            xml_file = file + '.xml'
            if xml_file in files:
                # image_id = image_id + 1
                annotation_path = os.path.abspath(os.path.join(root, xml_file))

                # tree = ET.parse(annotation_path)#.getroot()
                image = dict()
                # keyList = list()
                doc = xmltodict.parse(open(annotation_path).read())
                # print doc['annotation']['filename']
                image['file_name'] = coco_file_name  # str(doc['annotation']['filename'])
                # keyList.append("file_name")
                image['height'] = int(doc['annotation']['size']['height'])
                # keyList.append("height")
                image['width'] = int(doc['annotation']['size']['width'])
                # keyList.append("width")

                # image['id'] = str(doc['annotation']['filename']).split('.jpg')[0]
                image['id'] = image_id
                print("File Name: {} and image_id {}".format(xml_file, image_id))
                images.append(image)
                # keyList.append("id")
                # for k in keyList:
                # 	images1.append(images[k])
                # images2 = dict(zip(keyList, images1))
                # print images2
                # print images

                # attrDict["images"] = images

                # print attrDict
                # annotation = dict()
                id1 = 1
                if 'object' in doc['annotation']:
                    # 去除只有一个对象的图片
                    if type(doc['annotation']['object']) is list:
                        for obj in doc['annotation']['object']:
                            for value in attrDict["categories"]:
                                annotation = dict()
                                if image_id == 14 or image_id == 15:
                                    print("15 fail.")

                                # if str(obj['name']) in value["name"]:
                                if str(obj['name']) == value["name"]:
                                    # print str(obj['name'])
                                    # annotation["segmentation"] = []
                                    annotation["iscrowd"] = 0
                                    # annotation["image_id"] = str(doc['annotation']['filename']).split('.jpg')[0] #attrDict["images"]["id"]
                                    annotation["image_id"] = image_id
                                    x1 = int(obj["bndbox"]["xmin"]) - 1
                                    y1 = int(obj["bndbox"]["ymin"]) - 1
                                    x2 = int(obj["bndbox"]["xmax"]) - x1
                                    y2 = int(obj["bndbox"]["ymax"]) - y1
                                    annotation["bbox"] = [x1, y1, x2, y2]
                                    annotation["area"] = float(x2 * y2)
                                    annotation["category_id"] = value["id"]
                                    annotation["ignore"] = 0
                                    annotation["id"] = id1
                                    annotation["segmentation"] = [
                                        [x1, y1, x1, (y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2),
                                         y1]]
                                    id1 += 1

                                    annotations.append(annotation)

                else:
                    print("File: {} doesn't have any object".format(xml_file))
            # image_id = image_id + 1

            else:
                print("File: {} not found".format(file))

    attrDict["images"] = images
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"

    # print attrDict
    jsonString = json.dumps(attrDict)
    outputFile = os.path.join('COCO/annotations/', 'instances_'+tag+'.json')
    with open(outputFile, "w") as f:
        f.write(jsonString)


# rootDir = "/netscratch/pramanik/OBJECT_DETECTION/detectron/lib/datasets/data/Receipts/Annotations"
# for root, dirs, files in os.walk(rootDir):
# 	for file in files:
# 		if file.endswith(".xml"):
# 			annotation_path = str(os.path.abspath(os.path.join(root,file)))
# 			#print(annotation_path)
# 			generateVOC2Json(annotation_path)

"""
转换voc2007 to coco data format. 
VOC2007
  Annotations
    *.xml
  ImageSets/Main/test.txt       ---->
  ImageSets/Main/trainval.txt   ---->
  JPEGImages
    *.jpg

COCO
    annotations/
        instances_train2017.json
        instances_val2017.json
      train2017/
        COCO_train2017_*.jpg
      val2017/
        COCO_val2017_*.jpg
        
所以两件事情要做：
1.图片改名分别放在 train2017/ val2017/
2.生成xml 2 json
"""

# 先拿test做测试。
trainFile = "VOC2007/ImageSets//Main/trainval.txt" # trainval.txt \ test.txt

tag = 'train2017' # val2017\train2017
trainXMLFiles = list()
trainImages = list()
with open(trainFile, "rt") as f:
    for line in f:
        fileName = line.strip()
        print(fileName)
        trainXMLFiles.append(fileName)

rootDir = "VOC2007/Annotations"
generateVOC2Json(rootDir, trainXMLFiles, tag)
