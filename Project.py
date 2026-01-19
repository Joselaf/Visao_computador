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

img_hsv_h = img_hsv[:, :, 0]
img_hsv_S = img_hsv[:, :, 1]
img_hsv_V = img_hsv[:, :, 2]
HSV_S_eq = cv.equalizeHist(img_hsv_S)
HSV_V_eq = cv.equalizeHist(img_hsv_V) 

HSV_eq = np.zeros(img_hsv.shape, np.uint8)

HSV_eq[:, :, 0] = img_hsv_h
HSV_eq[:, :, 1] = HSV_S_eq
HSV_eq[:, :, 2] = HSV_V_eq

HSV_eq = cv.GaussianBlur(HSV_eq, (5,5), 0)
B = cv.cvtColor(HSV_eq, cv.COLOR_HSV2BGR)
B = cv.blur(B, (5,5))

plt.subplot(121)
plt.imshow(img)
plt.title("Imagem original")
plt.axis('off')
plt.subplot(122)
plt.imshow(B)
plt.title("Imagem melhorada")
plt.axis('off')
plt.show()
cv.waitKey(0)
cv.destroyAllWindows()

