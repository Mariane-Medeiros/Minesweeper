import random
import numpy as np

TAMANHO = 100
ROW, COLUMN = 10, 10
ADJACENTE = [(-1, -1), (-1, 0), (-1, +1), (0, -1),
             (0, +1), (+1, -1), (+1, 0), (+1, +1)]

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

# Exibe a matriz
print(matriz)
