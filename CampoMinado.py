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


clock = pygame.time.Clock()
windown = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Campo Minado')


class field:
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
espaco = 1
largura_total_matriz = COLUMN * largura_retangulo + (COLUMN - 1) * espaco
altura_total_matriz = ROW * altura_retangulo + (ROW - 1) * espaco

# Posição inicial para centralizar a matriz
x_inicial = (WIDTH - largura_total_matriz) // 2
y_inicial = (HEIGHT - altura_total_matriz) // 2


def desenhar_matriz():
    for i in range(ROW):
        for j in range(COLUMN):
            x = x_inicial + j * (largura_retangulo + espaco)
            y = y_inicial + i * (altura_retangulo + espaco)
            pygame.draw.rect(windown, cor_retangulo,
                             (x, y, largura_retangulo, altura_retangulo))
            pygame.draw.rect(
                windown, cor_linha, (x, y, largura_retangulo, altura_retangulo), 2)


def reveal_tile(x, y):
    x_posicao_final = x_inicial + largura_total_matriz
    y_posicao_final = y_inicial + altura_total_matriz
    if x >= x_inicial and x <= x_posicao_final and y >= y_inicial and y <= y_posicao_final:
        print('dsa')


def main():
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)
        desenhar_matriz()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            reveal_tile(x, y)


if __name__ == '__main__':
    main()
