import numpy as np

a = np.array([[5, 2, 9], [8, 10, 13], [15, 16, 1]])

print(a.size)
print(a.ndim)
print(a.shape)


matriz_transposta = np.transpose(a)
print(a)
print(matriz_transposta)
