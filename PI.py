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
num_labels = 0
labels = []
stats = []
centroids = []


def count_objects(img): ## função para contar o número de objetos
   img_copy = img.copy()
   gray = cv.cvtColor(img_copy, cv.COLOR_BGR2GRAY) ## passa imagem para tons de cizento
   gray = cv.GaussianBlur(gray,(5,5), 0) ## aplicamos a função para suavizar a imagem
   gray_for_circles = cv.medianBlur(gray, 5)  ## suaviza para detetar círculos
   img_bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY, cv.THRESH_OTSU)[1] ## aplica um treshold à imagem
   kernel = np.ones((5,5), np.uint8) ## criação de um kernel 
   img_bw = cv.morphologyEx(img_bw, cv.MORPH_ERODE, kernel) ## aplica por úçtimo uma erosão á imagem 
   circles = cv.HoughCircles(gray_for_circles, cv.HOUGH_GRADIENT_ALT, 1, 20, 50, 30, 0, 0)
   round_count = 0 if circles is None else len(circles[0])
   num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(img_bw, 8, cv.CV_32S)
   objects_info = []
   M_area = 0
   m_area = float("inf")
   obj_M_area = 1
   obj_m_area = 1
   x_M_area = 0
   y_M_area = 0
   x_m_area = 0
   y_m_area = 0
   w_M_area = 0
   h_M_area = 0
   w_m_area = 0
   h_m_area = 0
   round_count = 0
   for i in range(1, num_labels):
      (cx,cy) = centroids[i]
      mask = (labels == i).astype(np.uint8) * 255
      contours, hierarchy = cv.findContours(mask, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
      perimetro = cv.arcLength(contours[0], closed=True)
      area = stats[i, cv.CC_STAT_AREA]
      circularity = 0.0
      is_round = False
      if perimetro > 0:
         circularity = (4 * np.pi * area) / (perimetro ** 2)
         if circularity >= 0.9:
            is_round = True
            round_count += 1
      if hierarchy is not None and len(hierarchy) > 0:
         # holes are child contours of the outer contour (parent == 0)
         holes = max(int(np.count_nonzero(hierarchy[0][:, 3] == 0) - 1), 0)
      else:
         holes = 0
      x = stats[i, cv.CC_STAT_LEFT]
      y = stats[i, cv.CC_STAT_TOP]
      w = stats[i, cv.CC_STAT_WIDTH]
      h = stats[i, cv.CC_STAT_HEIGHT]
      area = stats[i, cv.CC_STAT_AREA]
      
      if(area < m_area):
         m_area = area
         obj_m_area = i
      elif(area > M_area):
         M_area = area
         obj_M_area = i
      x_M_area = stats[obj_M_area, cv.CC_STAT_LEFT]
      y_M_area = stats[obj_M_area, cv.CC_STAT_TOP]
      w_M_area = stats[obj_M_area, cv.CC_STAT_WIDTH]
      h_M_area = stats[obj_M_area, cv.CC_STAT_HEIGHT]
      x_m_area = stats[obj_m_area, cv.CC_STAT_LEFT]
      y_m_area = stats[obj_m_area, cv.CC_STAT_TOP]
      w_m_area = stats[obj_m_area, cv.CC_STAT_WIDTH]
      h_m_area = stats[obj_m_area, cv.CC_STAT_HEIGHT]
      objects_info.append({
         "id": int(i),
         "area": int(area),
         "perimeter": float(perimetro),
         "centroid": (int(cx), int(cy)),
         "bbox": (int(x), int(y), int(w), int(h)),
         "holes": holes,
         "is_round": bool(is_round)
      })
      cv.rectangle(img_copy, (x, y), (x + w, y + h), (255, 255, 255), 3)
      cv.putText(img_copy, f'.{i}', (int(cx), int(cy)), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255), 1)
   cv.rectangle(img_copy, (x_M_area, y_M_area), (x_M_area+ w_M_area, y_M_area + h_M_area), (255, 0, 0), 3)
   cv.rectangle(img_copy, (x_m_area, y_m_area), (x_m_area+ w_m_area, y_m_area + h_m_area), (0, 0, 255), 3)
   return(img_copy, num_labels-1, objects_info, round_count)


def Red_obj(img):
   img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) ##passa a para HSV a imagem 
   ## defenimos os intervalos do vermelho
   lower_red1  = np.array([0, 120, 70])
   lower_red2  = np.array([170, 120, 70])
   upper_red1  = np.array([10, 255, 255])
   upper_red2  = np.array([180, 255, 255])
   ## criamos as máscara
   mask1 = cv.inRange(img_HSV, lower_red1, upper_red1)
   mask2 = cv.inRange(img_HSV, lower_red2, upper_red2)
   ## combinamos as máscaras
   red_mask = cv.bitwise_or(mask1, mask2)
   ## aplicamos a máscara para extrair a cor
   result = cv.bitwise_and(img_HSV, img_HSV, mask=red_mask)
   ## cv.imshow("img",result)
   return (count_objects(result)[1])


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
   return (count_objects(result)[1])

def White_obj(img):
   img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV) ##passa a para HSV a imagem 
   ## Defenimos os intervalos do branco
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
   return (count_objects(result)[1])

def Round_obj(img):
   gray2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
   gray2 = cv.medianBlur(gray2, 5)
   circles = cv.HoughCircles(gray2, cv.HOUGH_GRADIENT_ALT, 1, 20, 50, 30, 0, 0)
   return(len(circles))

def build_objects_table(objects_info):
   if not objects_info:
      return "Nenhum objeto identificado."
   header = (
      f"{'ID':<5}"
      f"{'Area':<12}"
      f"{'Perimetro':<15}"
      f"{'Furos':<8}"
      f"{'Redondo':<10}"
      f"{'Centroide (x,y)':<20}"
      f"{'BBox (x,y,w,h)':<22}"
   )
   separator = "-" * len(header)
   lines = [header, separator]
   for obj in objects_info:
      cx, cy = obj["centroid"]
      x, y, w, h = obj["bbox"]
      lines.append(
         f"{obj['id']:<5}"
         f"{obj['area']:<12}"
         f"{obj['perimeter']:<15.2f}"
         f"{obj.get('holes', 0):<8}"
         f"{'sim' if obj.get('is_round') else 'nao':<10}"
         f"{f'({cx},{cy})':<20}"
         f"{f'({x},{y},{w},{h})':<22}"
      )
   return "\n".join(lines)


def plot_two_images(img,img2): ## função para plotar duas imagens lado a lado
   plt.subplot(121) ## Cria uma figura com duas subplots
   plt.imshow(img) ## Mostra a imagem original
   plt.title('Imagem Original') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.subplot(122) ## Seleciona a segunda subplot
   plt.imshow(img2) ## Mostra a imagem com o objeto encontrado
   plt.title('Caracteristicas Imagem') ## Adiciona um título à imagem
   plt.axis('off') ## Remove os eixos da imagem
   plt.show() ## Exibe as duas imagens lado a lado
   cv.waitKey(0)
   cv.destroyAllWindows()
   return   

def folder(folder): ## função para processar uma pasta de imagens
   for filename in os.listdir(folder): ## itera sobre todos os ficheiros na pasta
      route = os.path.join(folder,filename) ## cria o caminho completo do ficheiro
      img = cv.imread(route)  ## lê a imagem 
      file(img)

def file(img): ## função para processar um ficheiro de imagem
   img_obj_found, pecas_totais, objects_info, pecas_redondas = count_objects(img)  ## chama a função para encontrar o objeto na imagem
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
   print("\nTabela de objetos (extraída de count_objects):")
   print(build_objects_table(objects_info))
   plot_two_images(img_obj_found, img2)
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