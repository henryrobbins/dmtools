# misc_operations.py
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A.min())  # 1
print(A.max())  # 4
print(A.T)
# [[1 3]
#  [2 4]]
print(np.hstack((A,B)))
# [[1 2 5 6]
#  [3 4 7 8]]
print(np.vstack((A,B)))
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]