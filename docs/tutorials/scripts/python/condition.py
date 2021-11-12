# condition.py

x = True
y = False

print(x == True)   # True
print(x == False)  # False
print(x != False)  # True

print(not x)  # False

print(x & y)        # False
print(x & (not y))  # True
print(x | y)        # True
print((not x) | y)  # False

if True:
    print('True!')

if False:
    print('This will not print.')

if x | y:
    print('True!')
