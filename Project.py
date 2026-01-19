import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('Img.png')

img_hsv  = cv.cvtColor(img, cv.COLOR_BGR2HSV)
img_HSV_V = img_hsv[:,:,2]
img_HSV_S = img_hsv[:,:,1]

hist = cv.calcHist([img],[0], None, [256], [0, 256])

plt.hist(img.ravel(), 256, [0, 256])
plt.show()