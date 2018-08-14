import os
import cv2
import imutils


def draw_bordered_line(img, pt1, pt2, col1, col2, w1, w2):
    """Draw 2 overlaid lines to imitate a bordered line

    :param img: image to draw lines on
    :param pt1: tuple of (x, y) endpoint for line
    :param pt2: tuple of (x, y) endpoint for line
    :param col1: color for outer line
    :param col2: color for inner line
    :param w1: weight for outer line
    :param w2: weight for inner line
    :return: None; lines are drawn on image in place
    """
    cv2.line(img, pt1, pt2, col1, w1)
    cv2.line(img, pt1, pt2, col2, w2)


def is_integer(input_path):
    """Check if input can be safely coerced to integer

    intended for use with read_background to check if webcam index provided

    :param input_path: value to check if can be safely coerced to integer
    :return: (bool) True if can be safely assigned to be int; otherwise False
    """
    try:
        int_input = int(input_path)
        return int_input == float(input_path)
    except ValueError:
        return False


def read_background(input_path, background_width=600):
    """

    :param input_path:
    :param background_width:
    :return: (tuple) (background, input_type);
             background will be a cv2 image if input_path is an image, if input_path is a video then background is
             returned as a cv2.VideoCapture object
             input_type will be either 'video' or 'image' to specify what input the user passed
    """
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
