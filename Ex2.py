import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

A = cv.imread('Images/tulipas.jpg')
## Transformo a imagem  RGB para o espaço de cor HSV
HSV = cv.cvtColor(A, cv.COLOR_BGR2HSV)

## Dividir os canais de uma imagem HSV 
HSV_S = HSV[:, :, 1 ]
HSV_V = HSV[:, :, 2 ]
HSV_S_eq = cv.equalizeHist(HSV_S)
HSV_V_eq = cv.equalizeHist(HSV_V)

## Montar a imagem com os valores S e V equalizados e o H inalterado  
HSV_eq = np.zeros(HSV.shape, np.uint8)
HSV_eq[:, :, 0] = HSV[:, :, 0]
HSV_eq[:, :, 1] = HSV_S_eq
HSV_eq[:, :, 2] = HSV_V_eq

## Mostrar imagem equalizada 
B = cv.cvtColor(HSV_eq, cv.COLOR_HSV2BGR)
cv.imshow('Imagem EQ', B)
cv.waitKey(0)