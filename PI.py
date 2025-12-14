from tkinter import
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

def folder(folder): ## função para processar uma pasta de imagens
   for filename in os.listdir(folder): ## itera sobre todos os ficheiros na pasta
      route = os.path.join(folder,filename) ## cria o caminho completo do ficheiro
      img = cv.imread(route)  ## lê a imagem 
      img_with_obj = count_objects(img)  ## chama a função para encontrar o objeto na imagem
      plot_two_images(img, img_with_obj)  ## plota as duas imagens lado a lado


def file(img): ## função para processar um ficheiro de imagem
   img2 = count_objects(img)  ## chama a função para encontrar o objeto na imagem
   plot_two_images(img, img2)  ## plota as duas imagens lado a lado

def count_objects(img): ## função para contar o número de objetos
   gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) ## passa imagem para tons de cizento
   gray = cv.GaussianBlur(gray,(5,5), 0)
   img_bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY, cv.THRESH_OTSU)[1] ## aplica um treshold à imagem
   kernel = np.ones((5,5), np.uint8)
   img_bw = cv.morphologyEx(img_bw, cv.MORPH_ERODE, kernel)
   num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(img_bw, 8, cv.CV_32S)
   print(num_labels-1)
   return (img_bw)
       

def plot_two_images(img,img2): ## função para plotar duas imagens lado a lado
   plt.subplot(121) ## Cria uma figura com duas subplots
   plt.imshow(img) ## Mostra a imagem original
   plt.title('Imagem Original') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.subplot(122) ## Seleciona a segunda subplot
   plt.imshow(img2, cmap='gray') ## Mostra a imagem com o objeto encontrado
   plt.title('Imagem com Objeto Encontrado') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.show() ## Exibe as duas imagens lado a lado
   cv.waitKey(0)
   cv.destroyAllWindows()
   return


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