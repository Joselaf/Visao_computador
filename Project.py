import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

A = cv.imread('Img.png')

HSV = cv.cvtColor(A, cv.COLOR_BGR2HSV)

hist = cv.calcHist([A],[0], None, [256], [0, 256])

plt.hist(A.ravel(), 256, [0, 256])
plt.show()

HSV_S = HSV[:,:,1] ## retiramos o canal S da imagem HSV
HSV_V = HSV[:,:,2] ##retirmaos o canal V da imagem HSV
HSV_S_eq = cv.equalizeHist(HSV_S)  ## equalizamos o cabal S de HSV
HSV_V_eq = cv.equalizeHist(HSV_V)  ## equalizamos o canal V de HSV

HSV_eq = np.zeros(HSV.shape, np.uint8) ##criamos uma nova matriz para mostrar os valores equalizados em imagem
 ## Montamos a matriz com os seus valores devidos  
HSV_eq[:, :, 0] = HSV[:, : ,0] ## o primerio canal será o canal H inalterado
HSV_eq[:, :, 1] = HSV_S_eq ## o segundo canal será o canal S equalizado
HSV_eq[:, :, 2] = HSV_V_eq ## por último o terceiro canal será o canal V equalizado

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

