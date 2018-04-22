import numpy as np
t = np.linspace(0, 1, 11)
ch0 = np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/10
ch1 = np.cos(2*np.pi*t) + np.random.randn(t.shape[0])/10
ch2 = np.sin(2*np.pi*t) * np.cos(2*np.pi*t) + \
                                 np.random.randn(t.shape[0])/10 
data = np.transpose(np.vstack((t, ch0, ch1, ch2)))
print(data[0])