import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

A = cv.imread('Img.png')

HSV = cv.cvtColor(A, cv.COLOR_BGR2HSV)
HSV_S = HSV[:,:,1]
HSV_V = HSV[:,:,2]

hist = cv.calcHist([A],[0], None, [256], [0, 256])

plt.hist(A.ravel(), 256, [0, 256])
plt.show()

HSV_S_eq = cv.equalizeHist(HSV_S)
HSV_V_eq = cv.equalizeHist(HSV_V) 

HSV_eq = np.zeros(HSV.shape, np.uint8)

HSV_eq[:, :, 0] = HSV[:, : ,0]
HSV_eq[:, :, 1] = HSV_S_eq
HSV_eq[:, :, 2] = HSV_V_eq

HSV_eq = cv.GaussianBlur(HSV_eq, (5,5), 0)
B = cv.cvtColor(HSV_eq, cv.COLOR_HSV2BGR)
B = cv.GaussianBlur(B, (5,5), 0)

plt.subplot(121)
plt.imshow(A)
plt.title("Imagem original")
plt.axis('off')
plt.subplot(122)
plt.imshow(B)
plt.title("Imagem melhorada")
plt.axis('off')
plt.show()
cv.waitKey(0)
cv.destroyAllWindows()

