''' Contains primarily the functions for operating with vectors, which can be used in different situations. '''

import numpy as np

def originDist(x, y, z):
	''' Calculates the distance of a given point from the origin of the geocentric Cartesian coordinate system. 

		Arguments:
			x: [float] X coordinate of the 3D position (in m).
			y: [float] Y coordinate of the 3D position (in m).
			z: [float] Z coordinate of the 3D position (in m).
	
		Returns:
			r: [float] Distance from the origin (in m).
	'''

	r = np.sqrt(x**2 + y**2 + z**2)

	return r