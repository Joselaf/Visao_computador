import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

A = cv.imread('Images/tulipas.jpg')
HSV = cv.cvtColor(A, cv.COLOR_BGR2HSV)
HSV_S = HSV[:, :, 1 ]
HSV_V = HSV[:, :, 2 ]
HSV_S_eq = cv.equalizeHist(HSV_S)
HSV_V_eq = cv.equalizeHist(HSV_V)
HSV_eq = np.zeros(HSV.shape, np.uint8)
HSV_eq[:, :, 0] = HSV[:, :, 0]
HSV_eq[:, :, 1] = HSV_S_eq
HSV_eq[:, :, 2] = HSV_V_eq
B = cv.cvtColor(HSV_eq, cv.COLOR_HSV2BGR)
cv.imshow('Imagem EQ', B)
cv.waitKey(0)