# @Author  : lightXu
# @File    : sift_registration.py
# @Time    : 2019/5/24 0024 上午 10:21
import time
import cv2
import numpy as np


def resize_by_percent(im, percent):
    height = im.shape[0]
    width = im.shape[1]
    new_x = int(width * percent)
    new_y = int(height * percent)
    res = cv2.resize(im, (new_x, new_y), interpolation=cv2.INTER_AREA)
    return res


def sift_kp(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    kp_image = cv2.drawKeypoints(gray_image, kp, None)
    return kp_image, kp, des


def get_good_match(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)  # des1为模板图，des2为匹配图
    matches = sorted(matches, key=lambda x: x[0].distance / x[1].distance)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good


def sift_image_alignment(img1, img2, raw_img_regi, raw_width, raw_height, resize_ratio):
    _, kp1, des1 = sift_kp(img1)
    _, kp2, des2 = sift_kp(img2)
    t1 = time.time()
    good_match = get_good_match(des1, des2)
    t2 = time.time()
    print(t2-t1)
    img_out, transform_mtx, status = '', '', ''
    if len(good_match) > 4:
        ratio_array = np.array([resize_ratio, resize_ratio])  # 长宽压缩比列不同时
        ptsA = (np.float32([kp1[m.queryIdx].pt for m in good_match])*ratio_array).reshape(-1, 1, 2)
        ptsB = (np.float32([kp2[m.trainIdx].pt for m in good_match])*ratio_array).reshape(-1, 1, 2)

        transform_mtx, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold=4)
        img_out = cv2.warpPerspective(raw_img_regi, transform_mtx, (raw_width, raw_height),
                                     flags=cv2.INTER_AREA + cv2.WARP_INVERSE_MAP, borderValue=(255, 255, 255))
    return img_out, transform_mtx, status


if __name__ == '__main__':
    t1 = time.time()
    raw_img_template = cv2.imread(r'C:\Users\Administrator\Desktop\regi-test\001.jpg')
    raw_img_register = cv2.imread(r'C:\Users\Administrator\Desktop\regi-test\014.jpg')
    ratio = 0.5

    img_template = resize_by_percent(raw_img_template, ratio)
    img_register = resize_by_percent(raw_img_register, ratio)
    width, height = img_template.shape[1], img_template.shape[0]
    # 压缩后先计算匹配点，再映射至原始尺寸并计算转换矩阵，最后校准
    result, _, _ = sift_image_alignment(img_template, img_register, raw_img_register, width, height, ratio)
    cv2.imwrite(r'C:\Users\Administrator\Desktop\regi-test\014-1.jpg', result)
    t2 = time.time()
    print(t2 - t1)
