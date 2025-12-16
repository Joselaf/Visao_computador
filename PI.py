import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import sys
import os

pecas_totais = 0
pecas_vermelhas = 0
pecas_azuis = 0
pecas_brancas = 0
pecas_naodefinidas = 0
pecas_redondas = 0
M_area = 0
m_area = 0
obj_M_area = (0,0)
obj_m_area =(0,0)


def count_objects(img): ## função para contar o número de objetos
   gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) ## passa imagem para tons de cizento
   gray = cv.GaussianBlur(gray,(5,5), 0) ## aplicamos a função para suavizar a imagem
   img_bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY, cv.THRESH_OTSU)[1] ## aplica um treshold à imagem
   kernel = np.ones((5,5), np.uint8) ## criação de um kernel 
   img_bw = cv.morphologyEx(img_bw, cv.MORPH_ERODE, kernel) ## aplica por úçtimo uma erosão á imagem 
   num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(img_bw, 8, cv.CV_32S)
   for i in range(1, num_labels):
      (cx, cy) = centroids[i]
      mask = np.zeros_like(img_bw, np.uint8)
      mask[labels == i] = 255
      contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
      perimetro = cv.arcLength(contours[0], closed=True)
      x = stats[i, cv.CC_STAT_LEFT]
      y = stats[i, cv.CC_STAT_TOP]
      w = stats[i, cv.CC_STAT_WIDTH]
      h = stats[i, cv.CC_STAT_HEIGHT]
      area = stats[i, cv.CC_STAT_AREA]
      M_area = area
      m_area = area
      obj_M_area = centroids[i]
      obj_m_area = centroids[i]
      if(area < m_area):
         m_area = area
         obj_m_area = (x, y)
      elif(area > M_area):
         M_area = area
         obj_M_area = (x, y)
      cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 3)
   plot_two_images(img, gray)    
   return(num_labels-1)


def Red_obj(img):
   img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) ##passa a para HSV a imagem 
   ## Defenimos os intervalos do vermelho
   lower_red1  = np.array([0, 120, 70])
   lower_red2  = np.array([170, 120, 70])
   upper_red1  = np.array([10, 255, 255])
   upper_red2  = np.array([180, 255, 255])
   ##Criamos as máscara
   mask1 = cv.inRange(img_HSV, lower_red1, upper_red1)
   mask2 = cv.inRange(img_HSV, lower_red2, upper_red2)
   ##combinamos as máscaras
   red_mask = cv.bitwise_or(mask1, mask2)
   ##aplicamos a máscara para extrair a cor
   result = cv.bitwise_and(img_HSV, img_HSV, mask=red_mask)
   ##cv.imshow("img",result)
   return (count_objects(result))


def Blue_obj(img):
   img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) ##passa a para HSV a imagem 
   ## Defenimos os intervalos do azul
   lower_blue_1 = np.array([90, 50, 50])
   upper_blue_1 = np.array([110, 255, 255])
   lower_blue_2 = np.array([110, 50, 50])
   upper_blue_2 = np.array([140, 255, 255])
   ##Criamos as máscara
   mask1 = cv.inRange(img_HSV, lower_blue_1, upper_blue_1)
   mask2 = cv.inRange(img_HSV, lower_blue_2, upper_blue_2)
   ##Combinamos as máscaras
   blue_mask = cv.bitwise_or(mask1, mask2)
   ##aplicamos a máscara para extrair a cor
   result = cv.bitwise_and(img_HSV, img_HSV, mask=blue_mask)
   ##cv.imshow("img",result)
   return (count_objects(result))

def White_obj(img):
   img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) ##passa a para HSV a imagem 
   ## Defenimos os intervalos do vermelho
   lower_white1 = np.array([0, 0, 240])
   upper_white1 = np.array([179, 15, 255])
   lower_white2 = np.array([0, 0, 200])
   upper_white2 = np.array([179, 40, 255])
   ##Criamos as máscara
   mask1 = cv.inRange(img_HSV, lower_white1, upper_white1)
   mask2 = cv.inRange(img_HSV, lower_white2, upper_white2)
   ##combinamos as máscaras
   white_mask = cv.bitwise_or(mask1, mask2)
   ##aplicamos a máscara para extrair a cor
   result = cv.bitwise_and(img_HSV, img_HSV, mask=white_mask)
   ##cv.imshow("img",result)
   return (count_objects(result))



def plot_two_images(img,img2): ## função para plotar duas imagens lado a lado
   plt.subplot(121) ## Cria uma figura com duas subplots
   plt.imshow(img) ## Mostra a imagem original
   plt.title('Imagem Original') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.subplot(122) ## Seleciona a segunda subplot
   plt.imshow(img2, cmap='grey') ## Mostra a imagem com o objeto encontrado
   plt.title('Imagem com Objeto Encontrado') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.show() ## Exibe as duas imagens lado a lado
   cv.waitKey(0)
   cv.destroyAllWindows()
   return   

def folder(folder): ## função para processar uma pasta de imagens
   for filename in os.listdir(folder): ## itera sobre todos os ficheiros na pasta
      route = os.path.join(folder,filename) ## cria o caminho completo do ficheiro
      img = cv.imread(route)  ## lê a imagem 
      img_with_obj = count_objects(img)  ## chama a função para encontrar o objeto na imagem
      ##plot_two_images(img, img_with_obj)  ## plota as duas imagens lado a lado


def file(img): ## função para processar um ficheiro de imagem
   pecas_totais = count_objects(img)  ## chama a função para encontrar o objeto na imagem
   pecas_vermelhas = Red_obj(img)
   pecas_azuis = Blue_obj(img)
   pecas_brancas = White_obj(img)
   img_caracteristics = Image.new('RGB', (800, 600), color=(255, 255, 2555))
   img_caracteristics.save = ("Caractwerisitcas.png", 'PNG')
   img2 = np.array(img_caracteristics)
   cv.putText(img2,"pecas totais:" + str(pecas_totais), (0, 110),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   cv.putText(img2,"pecas vermelhas:" + str(pecas_vermelhas), (0, 190),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   cv.putText(img2,"pecas azuis:" + str(pecas_azuis), (0, 270),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   cv.putText(img2,"pecas brancas:" + str(pecas_brancas), (0, 350),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   cv.putText(img2,"pecas redondas:" + str(pecas_redondas), (0, 430),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   cv.putText(img2,"pecas nao defenidas:" + str(pecas_naodefinidas), (0, 510),cv.FONT_HERSHEY_COMPLEX,1,(0, 0, 0), 1)
   plot_two_images(img, img2)
   ##print("peças_totais:" + str(pecas_totais) +'\n' +"peças_vermelhas:" + str(pecas_vermelhas)+'\n' + "peças_azuis:" + str(pecas_azuis) + '\n' + "peças_bramcas:" + str(pecas_brancas) + '\n' + "peças_não_defenidas:" + str(pecas_naodefinidas))


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