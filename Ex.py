import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Load image in color mode (default)
A = cv.imread('Images/tulipas.jpg')
B = A[:, :, 0]
cv.calcHist([B],[0],None,[256],[0,256])
plt.hist(B.ravel(),256,[0,256])
plt.show()
B_eq = cv.equalizeHist(B)
cv.calcHist([B_eq], [0], None, [256], [0, 256])
plt.hist(B_eq.ravel(), 256, [0, 256])
plt.show()
