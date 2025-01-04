import pygame
from sys import exit
import random
import numpy as np

pygame.init()

run = True
WIDTH = 800
HEIGHT = 400
ROW, COLUMN = 10, 10
clock = pygame.time.Clock()
windown = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Campo Minado')


class field:
    bombs = [0, 1]
    randombombs = random.choices(bombs, weights=(80, 20), k=100)
    matrix = np.reshape(randombombs, (ROW, COLUMN))


def draw(windown):
    pass


def main():
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
