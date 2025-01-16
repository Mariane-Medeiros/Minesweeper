import pygame
from sys import exit
import random
import numpy as np

pygame.init()
TAMANHO = 100
ROW, COLUMN = 10, 10
ADJACENTE = [(-1, -1), (-1, 0), (-1, +1), (0, -1),
             (0, +1), (+1, -1), (+1, 0), (+1, +1)]
run = True
WIDTH = 1000
HEIGHT = 600
ROW, COLUMN = 10, 10
cor_retangulo = (190, 190, 190)
cor_linha = (255, 255, 255)
fonte = pygame.font.SysFont('Arial', 30)
ultimo_retangulo = []


clock = pygame.time.Clock()
windown = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Campo Minado')


class field:
    # MELHORAR ESSA CLASSE COM SELF
    randombombs = np.random.choice([0, 9], size=100, p=[0.8, 0.2])
    matriz = randombombs.reshape(10, 10)

    for i in range(matriz.shape[0]):  # Linha
        for j in range(matriz.shape[1]):  # Coluna
            if matriz[i][j] >= 9:
                for l in range(8):
                    linha = i + ADJACENTE[l][0]
                    coluna = j + ADJACENTE[l][1]
                    if linha < 0 or coluna < 0 or linha > 9 or coluna > 9:
                        pass
                    else:
                        matriz[linha][coluna] += 1


largura_retangulo = 35
altura_retangulo = 35
largura_total_matriz = COLUMN * largura_retangulo
altura_total_matriz = ROW * altura_retangulo

# Posição inicial para centralizar a matriz
matriz_x_inicial = (WIDTH - largura_total_matriz) // 2
matriz_y_inicial = (HEIGHT - altura_total_matriz) // 2
matriz_x_final = matriz_x_inicial + largura_total_matriz
matriz_y_final = matriz_y_inicial + altura_total_matriz
matriz_x_meio = matriz_x_inicial + (largura_total_matriz // 2)
matriz_y_meio = matriz_y_inicial + (altura_total_matriz // 2)
ROXO = (128, 0, 128)


def desenhar_tela():
    # print(ultimo_retangulo)
    for i in range(ROW):
        for j in range(COLUMN):
            x = matriz_x_inicial + j * largura_retangulo
            y = matriz_y_inicial + i * altura_retangulo
            pygame.draw.rect(windown, cor_retangulo,
                             (x, y, largura_retangulo, altura_retangulo))
            pygame.draw.rect(
                windown, cor_linha, (x, y, largura_retangulo, altura_retangulo), 2)
    if ultimo_retangulo:
        for i in ultimo_retangulo:
            x, y = i
            pygame.draw.rect(
                windown, ROXO, (x, y, largura_retangulo, altura_retangulo))
            pygame.display.update(
                (x, y, largura_retangulo, altura_retangulo))


def find_tile(x, y):
    global ultimo_retangulo
    if x < matriz_x_inicial or x > matriz_x_final or y < matriz_y_inicial or y > matriz_y_final:  # nao sei se o uso de or esta certo
        return
    x -= matriz_x_inicial
    rec_posicao_linha = x // largura_retangulo
    y -= matriz_y_inicial
    rec_posicao_coluna = y // altura_retangulo
    # calculo para acessar o primeiro ponto do novo retangulo
    x_rect = rec_posicao_linha * largura_retangulo + matriz_x_inicial
    y_rect = rec_posicao_coluna * altura_retangulo + matriz_y_inicial
    ultimo_retangulo.append((x_rect, y_rect))
    # reveal_tile(x_rect, y_rect)


def reveal_tile(x, y):
    pass


def main():
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
        desenhar_tela()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            find_tile(x, y)


if __name__ == '__main__':
    main()
