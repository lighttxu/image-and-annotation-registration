# @Author  : lightXu
# @File    : bbox_register.py
# @Time    : 2019/4/12 0012 下午 16:52
import math
import numpy as np


def bbox_register(scale, angle, shift, height, raw_box):
    """
        :param scale:
        :param angle:
        :param shift:
        :param height: height whole image
        :param raw_box: raw boundary box

    Returns:
        The transformed bbox
    """
    xmin = raw_box['xmin'] * scale
    ymin0 = raw_box['ymin']
    xmax = raw_box['xmax'] * scale
    ymax0 = raw_box['ymax']

    ymin = (height - ymax0) * scale
    ymax = (height - ymin0) * scale

    angle_mtx = np.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)],
    ])

    center_x = xmin + (xmax - xmin) // 2
    center_y = ymin + (ymax - ymin) // 2
    c = np.array([[center_x], [center_y]])

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

    return bbox
