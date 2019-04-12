# coding=utf-8
# @Author  : lightXu
# @File    : label_registration.py
# @Time    : 2019/4/11 0011 上午 10:40
import math
import os
import scipy as sp
import scipy.misc
import numpy as np
import glob2 as glob

import bbox_register
from .imreg_dft import imreg as ird
import xml.etree.cElementTree as ET


def crop_region(im, bbox):
    xmin = int(bbox['xmin'])
    ymin = int(bbox['ymin'])
    xmax = int(bbox['xmax'])
    ymax = int(bbox['ymax'])

    region = im[ymin:ymax, xmin:xmax]
    return region


def get_registration_para(img_as_template, img_for_registration):
    num_iter = 3
    res = ird.gen_similarity(img_as_template, img_for_registration, numiter=num_iter)

    y_shift, x_shift = -res['tvec'][0], res['tvec'][1]  # 原点在左下, y=-y(cv2原点在左上）
    shift = np.array([[x_shift], [y_shift]])
    # angle = res['angle'] * math.pi / 180  # 弧度
    angle = math.radians(res['angle'])
    scale = res['scale']

    return scale, angle, shift


def gen_registration_xml(roi_region, img_as_template, img_for_registration, xml_for_registration):
    t_region = crop_region(img_as_template, roi_region)
    r_region = crop_region(img_for_registration, roi_region)
    scale, angle, shift = get_registration_para(t_region, r_region)

    tree = ET.parse(xml_for_registration)
    root = tree.getroot()
    height = int(root.find('size').find('height').text)
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        bbox_dict = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        new_box = bbox_register.bbox_register(scale, angle, shift, height, bbox_dict)

        bbox.find('xmin').text = str(new_box['xmin'])
        bbox.find('ymin').text = str(new_box['ymin'])
        bbox.find('xmax').text = str(new_box['xmax'])
        bbox.find('ymax').text = str(new_box['ymax'])

    return tree


def register(img_dir, source_img_name, roi_region):
    find_str = os.path.join(img_dir, '*.jpg')
    source_img_path = os.path.join(img_dir, source_img_name)
    img_list = glob.glob(find_str)
    if source_img_path in img_list:
        img_list.remove(source_img_path)
    xml_source_path = source_img_path.replace('.jpg', '.xml')

    source_image = sp.misc.imread(source_img_path, True)
    for index, img_path in enumerate(img_list):
        image = sp.misc.imread(img_path, True)
        new_xml_path = img_path.replace('.jpg', '.xml')
        try:
            tree = gen_registration_xml(roi_region, image, source_image, xml_source_path)
            tree.write(new_xml_path)
            print(new_xml_path)
        except Exception:
            print('registration error: {}'.format(new_xml_path))


if __name__ == '__main__':
    img_dir_path = r'E:\dataset\third-part\P1\type1\2\even'
    source_img = '000776.jpg'
    roi = {'xmin': 270,
           'ymin': 530,
           'xmax': 520,
           'ymax': 600}

    register(img_dir_path, source_img, roi)
