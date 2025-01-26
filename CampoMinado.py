import inspect
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
BOMBPERCENTAGE = 0.15
SAFEPERCENTAGE = 0.85
propagate_empty_array = []
cor_retangulo = (190, 190, 190)
cor_linha = (255, 255, 255)
fonte = pygame.font.SysFont('Arial', 30)
ultimo_retangulo = []
numeros = []
BLACK = (0, 0, 0)
largura_retangulo = 35
altura_retangulo = 35
largura_total_matriz = COLUMN * largura_retangulo
altura_total_matriz = ROW * altura_retangulo
rec_posicao_linha, rec_posicao_coluna = 0, 0
bomb_img = pygame.image.load("assets/bomb.png")
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
def check_adjacent(l, c):
    for i in range(8):
        linha = l + ADJACENTE[i][0]
        coluna = c + ADJACENTE[i][1]
        if linha < 0 or coluna < 0 or linha >= ROW or coluna >= COLUMN:
            pass
        else:
            yield linha, coluna


class Field:

    def __init__(self):
        randombombs = np.random.choice([0, 9], size=TAMANHO, p=[
                                       SAFEPERCENTAGE, BOMBPERCENTAGE])
        self.matriz = randombombs.reshape(ROW, COLUMN)

    def run_matriz(self):
        for i in range(self.matriz.shape[0]):  # Linha
            for j in range(self.matriz.shape[1]):  # Coluna
                if self.matriz[i][j] >= 9:
                    for linha, coluna in check_adjacent(i, j):
                        self.matriz[linha][coluna] += 1
        return self.matriz


def game_over():
    windown.fill(BLACK)
    text = fonte.render("Game Over", True, ROXO)
    windown.blit(text, [(WIDTH // 2), (HEIGHT // 2)])


field = Field()
field.run_matriz()
print(field.matriz)
state_matriz_rec = np.zeros((ROW, COLUMN), dtype=int)
state_matriz_number = np.zeros((ROW, COLUMN), dtype=int)
state_matriz_propagation = np.zeros((ROW, COLUMN), dtype=int)


class Reveal_empty:
    def control_progation():
        # linha e coluna depende de quem vai chamar a matriz
        if field.matriz[rec_posicao_linha][rec_posicao_coluna] != 0:
            return
        else:
            # coloco ele pra o array nao iniciar vazio
            if state_matriz_propagation[rec_posicao_linha][rec_posicao_coluna] == 0:
                propagate_empty_array.append(
                    (rec_posicao_linha, rec_posicao_coluna))
                state_matriz_propagation[rec_posicao_linha][rec_posicao_coluna] = 1
            Reveal_empty.propagate_empty_cells()

    # PRECISO ADICIONAR IGNORAR DIAGONAIS
    def propagate_empty_cells():
        while len(propagate_empty_array) > 0:  # Enquanto houver elementos no array
            current_element = propagate_empty_array.pop(0)
            for linha, coluna in check_adjacent(current_element[0], current_element[1]):
                if state_matriz_propagation[linha][coluna] == 0:
                    if field.matriz[linha][coluna] == 0:
                        rect_drawing_coordinates(linha, coluna)
                        reveal_numbers(linha, coluna)
                        state_matriz_propagation[linha][coluna] = 1
                        propagate_empty_array.append((linha, coluna))
                    else:  # se eu bater em qualquer numero eu faço tudo menos colocar ele no array
                        rect_drawing_coordinates(linha, coluna)
                        reveal_numbers(linha, coluna)
                        state_matriz_propagation[linha][coluna] = 1


def put_flag():
    pass


def desenhar_tela():
    for i in range(ROW):
        for j in range(COLUMN):
            x = matriz_x_inicial + j * largura_retangulo
            y = matriz_y_inicial + i * altura_retangulo
            pygame.draw.rect(windown, cor_retangulo,
                             (x, y, largura_retangulo, altura_retangulo))
            pygame.draw.rect(
                windown, cor_linha, (x, y, largura_retangulo, altura_retangulo), 2)
    # desenha um retangulo por cima para sinalizar que ele foi clicado
    if ultimo_retangulo:
        for i in ultimo_retangulo:
            x, y = i
            pygame.draw.rect(
                windown, ROXO, (x, y, largura_retangulo, altura_retangulo))
            pygame.display.update(
                (x, y, largura_retangulo, altura_retangulo))
    # desenha o numero acima do retangulo
    if numeros:
        for i, numero in enumerate(numeros):
            if i < len(ultimo_retangulo):
                x, y = ultimo_retangulo[i]
                # Renderizar o número como string
                texto = fonte.render(str(numero), True, (255, 255, 255))
                if numero >= 9:
                    windown.blit(bomb_img, (x, y))
                    game_over()
                else:
                    windown.blit(texto, (x, y))


def find_tile(x, y):
    # pra poder acessar a posiçao que vamos desenhar os numeros
    global rec_posicao_linha, rec_posicao_coluna
    # saber se clicou fora da matriz
    if x < matriz_x_inicial or x > matriz_x_final or y < matriz_y_inicial or y > matriz_y_final:
        return
    # achar as cordenada relativas de x e y
    x -= matriz_x_inicial
    y -= matriz_y_inicial
    # divido o valor de x e y pelos retangulos para saber a linha e coluna
    rec_posicao_coluna = x // largura_retangulo
    rec_posicao_linha = y // altura_retangulo
    rect_drawing_coordinates(rec_posicao_linha, rec_posicao_coluna)
    reveal_numbers(rec_posicao_linha, rec_posicao_coluna)


def rect_drawing_coordinates(l, c):
    global ultimo_retangulo
    x_rect = c * largura_retangulo + matriz_x_inicial
    y_rect = l * altura_retangulo + matriz_y_inicial
    if state_matriz_number[l][c] == 0:
        ultimo_retangulo.append((x_rect, y_rect))
        state_matriz_number[l][c] = 1


def reveal_numbers(l, c):
    global numeros
    if state_matriz_rec[l][c] == 0:
        numero = field.matriz[l][c]
        numeros.append(numero)
        state_matriz_rec[l][c] = 1


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
            if event.button == 1:
                find_tile(x, y)
                Reveal_empty.control_progation()
            if event.button == 2:
                put_flag()


if __name__ == '__main__':
    main()
