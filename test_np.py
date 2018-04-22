import numpy as np

f_handle = file('my_file.dat', 'a')
np.savetxt(f_handle, my_matrix)
f_handle.close()