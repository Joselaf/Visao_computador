import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

def folder(folder):
   for filename in os.listdir(folder):
         Path = os.path.join(folder,filename) ## cria o caminho completo do ficheiro
         img = cv.imread(Path)  ## lê a imagem 
         img_with_obj = find_obj(img)  ## chama a função para encontrar o objeto na imagem
         plot_two_images(img, img_with_obj)  ## plota as duas imagens lado a lado


def file(img):
   img_with_obj = find_obj(img)  # chama a função para encontrar o objeto na imagem
   plot_two_images(img, img_with_obj)  # plota as duas imagens lado a lado


def find_obj(img):
   img_copy = img.copy() ## cria uma cópia da imagem original para desenhar o retângulo
   height,width = img.shape[:2] ## Obtém as dimensões da imagem
   x_CE = width // 4  ## Calcula as coordenadas do canto superior esquerdo do retângulo
   y_CE = height // 4 ## Calcula as coordenadas do canto superior esquerdo do retângulo
   x_CD = x_CE + width // 2 ## Calcula as coordenadas do canto inferior direito do retângulo
   Y_CD = y_CE  + height// 2 ## Calcula as coordenadas do canto inferior direito do retângulo
   cv.rectangle(img_copy, (x_CE,y_CE),(x_CD, Y_CD),(255,0,0),3) ## desenha um retângulo azul na imagem
   return img_copy ## retorna a imagem com o retângulo desenhado


def plot_two_images(img,img_copy):
   plt.subplot(121) ## Cria uma figura com duas subplots
   plt.imshow(img) ## Mostra a imagem original
   plt.title('Imagem Original') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.subplot(122) ## Seleciona a segunda subplot
   plt.imshow(img_copy) ## Mostra a imagem com o objeto encontrado
   plt.title('Imagem com Objeto Encontrado') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.show() ## Exibe as duas imagens lado a lado


def main():
   if(len(sys.argv) != 2): ## Verifica se um argumento foi passado
       print("Por favor, forneça o caminho de uma pasta ou arquivo de imagem como argumento.")
       return
   Folder_or_File = sys.argv[1] ## Obtém o argumento passado na linha de comando
   if os.path.isdir(Folder_or_File): ##Verifica se argumento é uma pasta
       folder(Folder_or_File) ## chama a função para processar a pasta
   elif os.path.isfile(Folder_or_File): ##Verifica se argumento é um ficheiro
         img = cv.imread(Folder_or_File)  ## lê a imagem
         file(img)  ## chama a função para processar o ficheiro
        
if __name__ == "__main__": ## Verifica se o script está a ser executado diretamente
    main() ## executa a secção do programa  main