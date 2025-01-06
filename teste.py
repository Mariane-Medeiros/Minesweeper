import random
import numpy as np

TAMANHO = 100
ROW, COLUMN = 10, 10

# bombs = [0, 9]
# randombombs = random.choices(bombs, weights=(80, 20), k=100)

list = [0] * TAMANHO

bombs = int(TAMANHO * 0.2)

# trocar para nome em ingles
indices_aleatorios = random.sample(range(TAMANHO), bombs)

print(indices_aleatorios)

# posso estar indo par aum lado negativo, antes da posiçao 0 com i-11
for i in indices_aleatorios:
    temp = i-11
    for j in range(3):
        list[j + temp] += 1

for i in indices_aleatorios:
    temp = i+9
    for j in range(3):
        if j + temp > len(list):
            pass
        else:
            list[j + temp] += 1

for i in indices_aleatorios:
    list[i] = 'B'

for i in range(len(list)):
    print(list[i], end=' ')  # Imprime o elemento e não pula linha
    if (i + 1) % 10 == 0:     # A cada 10 elementos, quebra a linha
        print()
