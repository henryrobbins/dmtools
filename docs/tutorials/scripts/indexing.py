# indexing.py
import numpy as np

A = np.array([0, 1, 2, 3, 4])

print(A[2:4])  # [2 3]
print(A[2:])   # [2 3 4]
print(A[:2])   # [0 1]
print(A[-2:])  # [3 4]

B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(B)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

print(B[1:])
# [[4 5 6]
#  [7 8 9]]
print(B[:, 1:])
# [[2 3]
#  [5 6]
#  [8 9]]
print(B[0:2, 0:2])
# [[1 2]
#  [4 5]]

C = np.zeros((3,3))
C[0:2, 0:2] = np.ones((2,2))
print(C)
# [[1. 1. 0.]
#  [1. 1. 0.]
#  [0. 0. 0.]]