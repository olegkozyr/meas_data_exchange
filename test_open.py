import numpy as np

with open('data3.txt', 'r') as _file:
    print(_file.readline()[:-1])
    print(_file.readline()[:-1])
    for f in _file:
        print(f.split())