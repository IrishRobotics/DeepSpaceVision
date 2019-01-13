import cv2
import gui

import argparse

parser = argparse.ArgumentParser(description='Threshold some images')
parser.add_argument('image', type=str, help='Path to an image')
args = parser.parse_args()

image = cv2.imread(args.image)

while True:
    gui.display(image)
    try:
        gui.refresh()
    except KeyboardInterrupt:
        break

gui.close()
