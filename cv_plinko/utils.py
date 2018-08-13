import os
import cv2
import imutils


def draw_bordered_line(img, pt1, pt2, col1, col2, w1, w2):
    cv2.line(img, pt1, pt2, col1, w1)
    cv2.line(img, pt1, pt2, col2, w2)


def is_integer(input_path):
    try:
        int_input = int(input_path)
        return int_input == float(input_path)
    except ValueError:
        return False


def read_background(input_path, background_width=600):
    if is_integer(input_path):
        background = cv2.VideoCapture(int(input_path))
        input_type = 'video'
    else:
        _, extension = os.path.splitext(input_path)
        if extension in [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]:
            background = cv2.imread(input_path)
            background = imutils.resize(background, width=background_width)
            input_type = 'image'
        else:
            background = cv2.VideoCapture(input_path)
            input_type = 'video'

    return background, input_type
