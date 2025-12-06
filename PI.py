import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys

def find_obj(img):
   img_copy = img.copy()
   height,width = img.shape[:2]
   print(height,width)
   x_CE = width // 4
   y_CE = height // 4
   x_CD = x_CE + width // 2
   Y_CD = y_CE  + height// 2
   cv.rectangle(img_copy, (x_CE,y_CE),(x_CD, Y_CD),(255,0,0),3) # desenha um retângulo azul na imagem))
   return img_copy

def plot_two_images(img,img_copy):
   plt.subplot(121)
   plt.imshow(img)
   plt.title('Imagem Original')
   plt.axis('off')
   plt.subplot(122)
   plt.imshow(img_copy)
   plt.title('Imagem com Objeto Encontrado')
   plt.axis('off')
   plt.show()

def main():
   Path = sys.argv[1]  ## caminho da imagem
   img = cv.imread(Path)  # lê a imagem
   img_with_obj = find_obj(img)  # chama a função para encontrar o objeto na imagem
   plot_two_images(img, img_with_obj)  # plota as duas imagens lado a lado
   # plt.subplot(121)
   # plt.imshow(img)
   # plt.title('Imagem Original')
   # plt.axis('off')
   # plt.subplot(122)
   # plt.imshow(img_with_obj)
   # plt.title('Imagem com Objeto Encontrado')
   # plt.axis('off')
   # plt.show()
   # plt.waitkey(0)
   # plt.destroyAllWindows()

   # cv.rectangle(img, (5,5),(200,200),(255,0,0),3) # desenha um retângulo azul na imagem))
   # cv.imshow('Imagem Original', img) # exibe a imagem original
   # cv.waitKey(0) # espera uma tecla ser pressionada
   # cv.destroyAllWindows() # fecha todas as janelas abertas pelo OpenCV



    





if __name__ == "__main__":
    main() # executa a parte principal do programa "main"

