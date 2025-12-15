import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('shapes.png')  ## lê a imagem
gay = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  ## converte a imagem para escala de cinza
img_bw = cv.threshold(gay, 10, 255, cv.THRESH_BINARY)[1]  ## aplica um limiar para obter uma imagem binária
kernel = np.ones((5,5),np.uint8)  ## cria um kernel para operações morfológicas
img_bw = cv.morphologyEx(img_bw, cv.MORPH_CLOSE, kernel)  ## aplica a operação morfológica de fechamento
num_labels_1, labels_im_1 = cv.connectedComponents(img_bw, connectivity=8, ltype=cv.CV_32S)  ## encontra os componentes conectados na imagem binária
print(str(num_labels_1-1) + " objetos encontrados")  ## imprime o número de objetos encontrados (excluindo o fundos)
num_labels_2, lbels_im2, stats, centroids = cv.connectedComponentsWithStats(img_bw, connectivity=8, ltype=cv.CV_32S)  ## encontra os componentes conectados com estatísticas adicionais
for i in range(1, num_labels_2):  ## itera sobre cada componente conectado (excluindo o fundo)
    x = stats[i, cv.CC_STAT_LEFT]  ## obtém a coordenada x do canto superior esquerdo do retângulo delimitador
    y = stats[i, cv.CC_STAT_TOP]  ## obtém a coordenada y do canto superior esquerdo do retângulo delimitador
    w = stats[i, cv.CC_STAT_WIDTH]  ## obtém a largura do retângulo delimitador
    h = stats[i, cv.CC_STAT_HEIGHT]  ## obtém a altura do retângulo delimitador
    area = stats[i, cv.CC_STAT_AREA]  ## obtém a área do componente conectado
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  ## desenha um retângulo ao redor do componente conectado na imagem original
    cv.putText(img, f'Area: {area}', (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  ## adiciona o texto da área acima do retângulo
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))  ## converte a imagem de BGR para RGB e exibe-a
plt.title('Imagem com Objetos Encontrados')  ## adiciona um título à imagem
plt.axis('off')  ## remove os eixos da imagem
plt.show()  ## exibe a imagem com os objetos encontrados
cv.waitKey(0)  ## espera por uma tecla ser pressionada
cv.destroyAllWindows()  ## fecha todas as janelas abertas pelo OpenCV


    