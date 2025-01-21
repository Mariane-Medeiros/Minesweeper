import pygame
from sys import exit
import random
import numpy as np

pygame.init()
ROW, COLUMN = 15, 15
TAMANHO = ROW * COLUMN
ADJACENTE = [(-1, -1), (-1, 0), (-1, +1), (0, -1),
             (0, +1), (+1, -1), (+1, 0), (+1, +1)]
run = True
WIDTH = 1000
HEIGHT = 600
cor_retangulo = (190, 190, 190)
cor_linha = (255, 255, 255)
fonte = pygame.font.SysFont('Arial', 30)
# Variáveis globais
ultimo_retangulo = []
numeros = []
x_rect = 0
y_rect = 0
contador = 0

largura_retangulo = 35
altura_retangulo = 35
largura_total_matriz = COLUMN * largura_retangulo
altura_total_matriz = ROW * altura_retangulo
rec_posicao_linha, rec_posicao_coluna = 0, 0

# Posição inicial para centralizar a matriz
matriz_x_inicial = (WIDTH - largura_total_matriz) // 2
matriz_y_inicial = (HEIGHT - altura_total_matriz) // 2
matriz_x_final = matriz_x_inicial + largura_total_matriz
matriz_y_final = matriz_y_inicial + altura_total_matriz
matriz_x_meio = matriz_x_inicial + (largura_total_matriz // 2)
matriz_y_meio = matriz_y_inicial + (altura_total_matriz // 2)
ROXO = (128, 0, 128)


clock = pygame.time.Clock()
windown = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Campo Minado')


@staticmethod
def check_adjacent(i, j):
    for l in range(8):
        linha = i + ADJACENTE[l][0]
        coluna = j + ADJACENTE[l][1]
        yield linha, coluna


class Field:
    linha = 0
    coluna = 0

    def __init__(self):
        randombombs = np.random.choice([0, 9], size=TAMANHO, p=[0.8, 0.2])
        self.matriz = randombombs.reshape(ROW, COLUMN)

    def run_matriz(self):
        for i in range(self.matriz.shape[0]):  # Linha
            for j in range(self.matriz.shape[1]):  # Coluna
                if self.matriz[i][j] >= 9:
                    for linha, coluna in check_adjacent(i, j):
                        if linha < 0 or coluna < 0 or linha >= ROW or coluna >= COLUMN:
                            print(coluna)
                            pass
                        else:
                            self.matriz[linha][coluna] += 1
        return self.matriz


field = Field()
field.run_matriz()
state_matriz = np.zeros((ROW, COLUMN), dtype=int)


class Reveal_empty:

    def propagate_empty_cells():
        global rec_posicao_linha, rec_posicao_coluna

    check_adjacent()


def desenhar_tela():
    global contador
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
    if numeros:
        for i, numero in enumerate(numeros):
            if i < len(ultimo_retangulo):
                x, y = ultimo_retangulo[i]
                # Renderizar o número como string
                texto = fonte.render(str(numero), True, (255, 255, 255))
                windown.blit(texto, (x, y))


def find_tile(x, y):
    global x_rect, y_rect  # pra poder acessar a posiçao que vamos desenhar os numeros
    global ultimo_retangulo
    global rec_posicao_linha, rec_posicao_coluna
    # saber se clicou fora da matriz
    if x < matriz_x_inicial or x > matriz_x_final or y < matriz_y_inicial or y > matriz_y_final:
        return
    # achar as cordenada relativas de x e y
    x -= matriz_x_inicial
    y -= matriz_y_inicial
    # divido o valor de x e y pelos retangulos para saber a linha e coluna
    rec_posicao_linha = x // largura_retangulo
    rec_posicao_coluna = y // altura_retangulo
    # SEPARA DO RESTANTE calculo para acessar o primeiro ponto do novo retangulo(para poder desenhar)
    x_rect = rec_posicao_linha * largura_retangulo + matriz_x_inicial
    y_rect = rec_posicao_coluna * altura_retangulo + matriz_y_inicial
    ultimo_retangulo.append((x_rect, y_rect))
    reveal_tile(rec_posicao_linha, rec_posicao_coluna)
    Reveal_empty.propagate_empty_cells()


def reveal_tile(l, c):
    global numeros
    # pegando o retangulo que esta posicionado na linha e coluna que eu quero e colocando no array para se desenhado
    numero = field.matriz[l][c]
    numeros.append(numero)
    return


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
