# numpy_array.py
import numpy as np

x = [1, 2, 3]
y = np.array([1, 2, 3])

print(x)     # [1, 2, 3]
print(y)     # [1 2 3]
print(x[0])  # 1
print(y[0])  # 1

print(x + x) # [1, 2, 3, 1, 2, 3]
print(y + y) # [2 4 6]

w = np.zeros(3)
z = np.ones((2, 2))
print(w)  # [0. 0. 0.]
print(z)
# [[1. 1.]
#  [1. 1.]]