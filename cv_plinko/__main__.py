import argparse
import cv2
import imutils
from .plinko_board_class import PlinkoBoard

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True,
                help='Path to input image to be used as game board.')
ap.add_argument('-w', '--width', default=600, type=int,
                help='Width to resize input image to (use 0 no resize)')
args = vars(ap.parse_args())

image = cv2.imread(args['input'])
if args['width'] > 0:
    image = imutils.resize(image, width=args['width'])

plinko = PlinkoBoard(image)
plinko.play()
