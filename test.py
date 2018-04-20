import numpy as np

with open('data1.txt', 'w') as f:
    t = np.arange(0, 1, 0.1)
    y = np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/10
    z = np.cos(2*np.pi*t) + np.random.randn(t.shape[0])/10
    for x1, x2, x3 in zip(t, y, z):
        f.write('{:.4f} {:.4f} {:.4f}{}'.format(x1, x2, x3, '\n'))
