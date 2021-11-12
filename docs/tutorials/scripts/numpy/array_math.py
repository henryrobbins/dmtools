# array_math.py
import numpy as np

A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

print(A + B)  # [5 7 9]
print(B - A)  # [3 3 3]
print(A * B)  # [ 4 10 18]
print(B / A)  # [4.  2.5 2. ]

print(np.power(A,2))  # [1 4 9]
print(np.sin(A))      # [0.84147098 0.90929743 0.14112001]
