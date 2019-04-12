# @Author  : lightXu
# @File    : registration_demo.py
# @Time    : 2019/4/10 0010 上午 10:46
import math
import cv2

import scipy as sp
import scipy.misc
import numpy as np

from imreg_dft import imreg as ird


def get_para():
    img1_path = r'C:\Users\Administrator\Desktop\regi\sample1.png'
    img2_path = r'C:\Users\Administrator\Desktop\regi\sample3.png'

    im0 = sp.misc.imread(img1_path, True)
    # the image to be transformed
    im1 = sp.misc.imread(img2_path, True)

    # im0 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    # im1 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    result = ird.similarity(im0, im1, numiter=3)

    timg = result['timg']
    # # cv2.imshow('timg', timg)
    # # if cv2.waitKey(0) == 27:
    # #     cv2.destroyAllWindows()
    img_save_path = img1_path.replace('000005', '000001_to_000005_saved')
    cv2.imwrite(img_save_path, timg)
    #
    # # Maybe we don't want to show plots all the time
    # if os.environ.get("IMSHOW", "no") == "yes":
    #     import matplotlib.pyplot as plt
    #     ird.imshow(im0, im1, timg)
    #     plt.show()
    print(result)
    return result


def gen_new_xml():
    height = 92
    res = get_para()  # 原点在左下

    y_shift, x_shift = -res['tvec'][0], res['tvec'][1]
    shift = np.array([[x_shift], [y_shift]])
    # angle = res['angle'] * math.pi / 180  # 弧度
    angle = math.radians(res['angle'])
    scale = res['scale']

    xmin = 93 * scale
    ymin0 = 54
    xmax = 146 * scale
    ymax0 = 64

    ymin = (height - ymax0) * scale
    ymax = (height - ymin0) * scale

    angle_mtx = np.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)],
    ])

    center_x = xmin + (xmax - xmin) // 2
    center_y = ymin + (ymax - ymin) // 2
    c = np.array([
        [center_x],
        [center_y],
    ])

    vertex_list = [np.array([[xmin], [ymin]]),
                   np.array([[xmax], [ymin]]),
                   np.array([[xmax], [ymax]]),
                   np.array([[xmin], [ymax]]), ]

    x_coordinate_list = []
    y_coordinate_list = []
    for ele in vertex_list:
        out_vertex = np.dot(angle_mtx, ele - c) + c + shift
        x_coordinate_list.append(out_vertex[0])
        y_coordinate_list.append(height - out_vertex[1])

    bbox = {'xmin': int(min(x_coordinate_list)), 'ymin': int(min(y_coordinate_list)),
            'xmax': int(max(x_coordinate_list)), 'ymax': int(max(y_coordinate_list))}

    print(bbox)


# gen_new_xml()


def try_reg():
    height = 300

    xmin = 122
    ymin0 = 132
    xmax = 1083
    ymax0 = 224

    ymin = height - ymax0
    ymax = height - ymin0

    c = np.array([[xmin + (xmax - xmin) // 2],
                  [ymin + (ymax - ymin) // 2]])

    angle_num = 0.01122525649756767
    angle = angle_num * math.pi / 180  # 弧度

    angle_mtx = np.array([[math.cos(angle), -math.sin(angle)],
                          [math.sin(angle), math.cos(angle)]])

    out = np.dot(angle_mtx, (np.array([[xmin], [ymin]]) - c)) + c

    out1 = np.dot(angle_mtx, (np.array([[xmax], [ymax]]) - c)) + c

    bias = np.array([[5.9467022], [-6.08038524]])

    print(out + bias)
    print(out1 + bias)


def similarity_matrix(scale, angle, vector):
    """
    Return homogeneous transformation matrix from similarity parameters.

    Transformation parameters are: isotropic scale factor, rotation angle (in
    degrees), and translation vector (of size 2).

    The order of transformations is: scale, rotate, translate.

    """
    # raise NotImplementedError("We have no idea what this is supposed to do")
    m_scale = np.diag([scale, scale, 1.0])
    m_rot = np.identity(3)
    angle = math.radians(angle)
    m_rot[0, 0] = math.cos(angle)
    m_rot[1, 1] = math.cos(angle)
    m_rot[0, 1] = -math.sin(angle)
    m_rot[1, 0] = math.sin(angle)
    m_transl = np.identity(3)
    m_transl[:2, 2] = vector
    res = np.dot(m_transl, np.dot(m_rot, m_scale))
    print(res)
    return res


angle0 = -30.086047819656727
scale0 = 1.2502392115796053
tvec0 = np.array([72.72131017, 34.86251252])
similarity_matrix(angle0, scale0, tvec0)

# try_reg()
