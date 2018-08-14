import cv2
import numpy as np


class Gate:
    """Class to simulate falling plinko game pieces

    Not intended for general usage

    :param x0: x coord of gate upper left corner
    :param x1: x coord of gate upper right corner
    :param y0: y coord of gate upper left corner
    :param y1: y coord of gate upper right corner
    """
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

        self.value = np.random.choice([10, 50, 100, 500], p=[0.48, 0.3, 0.2, 0.02])

    def in_gate(self, xy):
        """Check if an (x, y) tuple is in bounds of gate dims

        :param xy: tuple of coordinates
        :return: (bool) True if xy is in bounds of gate corners; otherwise False
        """
        x, y = tuple(xy)
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def draw(self, image):
        """Draw gate overlaid on input image

        :param image: BGR cv2 image to draw gate value and edges on
        :return: None; image is modified in place
        """
        cv2.putText(image, str(self.value), (self.x0 + 3, self.y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (250, 250, 250), thickness=2)
        cv2.putText(image, str(self.value), (self.x0 + 3, self.y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), thickness=1)

        cv2.line(image, (self.x1, self.y1), (self.x1, self.y0), (255, 255, 255), 3)
        cv2.line(image, (self.x1, self.y1), (self.x1, self.y0), (0, 0, 0), 1)
