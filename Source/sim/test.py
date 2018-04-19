import numpy as np 

def r(x, alpha):
	alpha = np.deg2rad(alpha)
	return x * np.sin(alpha) / (np.cos(alpha)**2)

v = r(-1, 170)
print(v)