# array_attributes.py
import numpy as np

A = np.array([[1, 2, 3],[4, 5, 6]])
print(A)
# [[1 2 3]
#  [4 5 6]]

print(A.ndim)   # 2
print(A.size)   # 6
print(A.shape)  # (2, 3)

B = np.array([[[1,2],[3,4]],[[5,6],[7,8]]])
print(B)
# [[[1 2]
#   [3 4]]
#
#  [[5 6]
#   [7 8]]]

print(B.ndim)   # 3
print(B.size)   # 8
print(B.shape)  # (2, 2, 2)
