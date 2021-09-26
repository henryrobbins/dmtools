# list_comprehension.py

# without list comprehension

x = []  # this list is empty
for i in range(4):
    x.append(i)
print(x)  # [0, 1, 2, 3]

# with list comprehension

x = [i for i in range(4)]
print(x)  # [0, 1, 2, 3]

y = [i**2 for i in range(4) if i**2 != 4]
print(y)  # [0, 1, 9]
