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

# for i in indices_aleatorios:
#    temp = i-11
#    for j in range(3):
#        list[j + temp] += 1

for i in indices_aleatorios:
    anterior = i-11
    posterior = i+9
    loops = 3

    bomba_inicio = True if i % 10 == 0 else False

    bomba_final = True if (i + 1) % 10 == 0 else False
    # checar como ele esta lidando com o primeiro e ultimo numero

    if bomba_inicio:
        anterior = i - 10
        posterior = i + 10
    else:
        if (i-1) > 0:
            list[i-1] += 1

    if bomba_final:
        loops = 2
    else:
        if (i+1) > len(list) - 1:
            list[i+1] += 1

    for j in range(loops):
        if not (j + posterior > len(list) - 1 or j + posterior > len(list) - 1):
            list[j + posterior] += 1
            if (j + anterior) > 0:
                list[j + anterior] += 1


for i in indices_aleatorios:
    list[i] = 'B'

for i in range(len(list)):
    print(list[i], end=' ')  # Imprime o elemento e não pula linha
    if (i + 1) % 10 == 0:     # A cada 10 elementos, quebra a linha
        print()
