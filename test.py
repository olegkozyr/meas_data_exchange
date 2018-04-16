import numpy as np

with open('data2.txt', 'w') as f:
    x1 = np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/10
    f.write('{:.4f} {:.4f} {:.4f} {}'.format(2.4, 5.666, '\n'))