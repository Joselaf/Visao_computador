import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

def folder(folder):
   for filename in os.listdir(folder):
         Path = os.path.join(folder,filename)
         img = cv.imread(Path)  # lê a imagem
         img_with_obj = find_obj(img)  # cshama a função para encontrar o objeto na imagem
         plot_two_images(img, img_with_obj)  # plota as duas imagens lado a lado


def file(img):
   img_with_obj = find_obj(img)  # chama a função para encontrar o objeto na imagem
   plot_two_images(img, img_with_obj)  # plota as duas imagens lado a lado


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
   if(len(sys.argv) != 2): ## Verifica se um argumento foi passado
       print("Por favor, forneça o caminho de uma pasta ou arquivo de imagem como argumento.")
       return
   Folder_or_File = sys.argv[1]
   if os.path.isdir(Folder_or_File): ##Verifica se argumento é uma pasta
       folder(Folder_or_File)
   elif os.path.isfile(Folder_or_File): ##Verifica se argumento é um ficheiro
         img = cv.imread(Folder_or_File)  # lê a imagem
         file(img)
        
if __name__ == "__main__":
    main() # executa a secção do programa  main

