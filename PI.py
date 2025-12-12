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
   img_with_obj = count_objects(img)  ## chama a função para encontrar o objeto na imagem
   plot_two_images(img, img_with_obj)  ## plota as duas imagens lado a lado

def count_objects(img): ## função para contar o número de objetos
   gray =cv.fastNlMeansDenoising(cv.cvtColor(img, cv.COLOR_BGR2GRAY)) ## passa imagem para tons de cizento
   img_bw = cv.threshold(gray, 55, 255, cv.THRESH_BINARY)[1] ## aplica um treshold à imagem 
   kernel = np.ones((3,3),np.uint8) ## criação de um kernel 
   img_bw = cv.morphologyEx(img_bw, cv.MORPH_OPEN, kernel) ## aplica um processo morfológico de abertura à imagem 
   img_bw = cv.morphologyEx(img_bw, cv.MORPH_CLOSE, kernel)## aplica um processo morfológico de fecho à imagem 
   img_bw = cv.erode(img_bw, kernel, iterations=1) ## aplica erosão à imagem 
   num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(img_bw, 8, cv.CV_32S)  ## extrai da imagem informção pertinente
   for i in range(1, num_labels):
      x = stats[i, cv.CC_STAT_LEFT] 
      y = stats[i, cv.CC_STAT_TOP]
      w = stats[i, cv.CC_STAT_WIDTH]
      h = stats[i, cv.CC_STAT_HEIGHT]
      area = stats[i, cv.CC_STAT_AREA]
      (cx, cy) = centroids[i]
      cv.circle(img, (int(cx), int(cy)), 3, (0, 0, 0), -1)
      ##cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
      ##cv.putText(img, f'Area: {area}', (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
   print(num_labels)
   return (img)
       
       

def stats_obj(img): ## função para encontrar o objeto na imagem e retornar a imagem com o objeto encontrado
    
    count_objects(img)  ## chama a função para contar o número de objetos

def plot_two_images(img,img_copy): ## função para plotar duas imagens lado a lado
   plt.subplot(121) ## Cria uma figura com duas subplots
   plt.imshow(img) ## Mostra a imagem original
   plt.title('Imagem Original') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.subplot(122) ## Seleciona a segunda subplot
   plt.imshow(img_copy,cmap='gray') ## Mostra a imagem com o objeto encontrado
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