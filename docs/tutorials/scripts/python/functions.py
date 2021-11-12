# functions.py

# this function returns something
def add(x, y):
    return x + y

x = add(2,3)
y = add(7,8)
print(x)       # 5
print(y)       # 15

# this function does not return anything
def append_one(x):
    x.append(1)

x = [4, 3, 2]
y = append_one(x)
print(x)       # [4, 3, 2, 1]
print(y)       # None
