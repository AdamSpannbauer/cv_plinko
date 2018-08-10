import numpy as np


class Gate:
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

        self.value = np.random.choice([10, 50, 100, 500], p=[0.4, 0.3, 0.2, 0.1])

    def in_gate(self, xy):
        x, y = tuple(xy)
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1
