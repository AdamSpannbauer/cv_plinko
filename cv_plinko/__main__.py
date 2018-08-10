import argparse
import cv2
from .plinko_board import create_edge_map

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', default='../images/pyimage_combo.png',
                help='Path to input image to be used as game board.')
args = vars(ap.parse_args())

image = cv2.imread(args['input'])
edge_map = create_edge_map(image)

cv2.imshow('...', image)
cv2.waitKey(0)
