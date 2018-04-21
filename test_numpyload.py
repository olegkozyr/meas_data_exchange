import numpy as np

with open('data3.txt', 'r') as f:
    print(f.readline().split())
    print(f.readline().split())
print(np.genfromtxt('data3.txt', skip_header=2))
