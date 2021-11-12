# condition_array.py
import numpy as np

A = np.array([1, 2, 3, 4, 5])

print(A > 2)     # [False False True True True]
print(A[A > 2])  # [3 4 5]

B = np.array([[1, 2], [3, 4]])

print(B < 4)
# [[ True  True]
#  [ True False]]
print(B[B < 4])  # [1 2 3]
