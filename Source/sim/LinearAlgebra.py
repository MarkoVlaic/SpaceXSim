''' Contains primarily the functions for operating with vectors, which can be used in different situations. '''

import numpy as np

def originDist(x, y, z):
	''' Calculates the distance of a given point from the origin of the geocentric Cartesian coordinate system. 

		Arguments:
			x: [float] X coordinate of the 3D position.
			y: [float] Y coordinate of the 3D position.
			z: [float] Z coordinate of the 3D position.
	
		Returns:
			r: [float] Distance from the origin.
	'''

	r = np.sqrt(x**2 + y**2 + z**2)

	return r

def sphericalToCartesian(r, phi, theta):
	''' Converts the coordinates from the spherical coordinate system analog to (lat, lon, h)
			to Cartesian (x, y, z) coordinates. 

		Arguments:
			r: [float] Distance from the origin / Vector magnitude (m).	
			phi: [float] Angle measured counterclockwise from the X axis to the orthogonal projection of vector.	
			theta: [float] Angle measured counterclockwise from the Z axis. 

		Return:
			position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object. (m, m, m)

	'''

	# Calculate Cartesian coordinates
	x = r * np.cos(phi) * np.cos(theta)
	y = r * np.cos(phi) * np.sin(theta)
	z = r * np.sin(phi)

	position = (x, y, z)

	return position

def cartesianToSpherical(x, y, z):
	''' Converts Cartesian coordinates to spherical coordinate system coordinates. 

		Arguments:
			x: [float] Position of the point along the X axis.
			y: [float] Position of the point along the Y axis.
			z: [float] Position of the point along the Z axis.
	
		Return:
			position: [tuple of floats] A tuple of (r, theta, phi) spherical coordinates. 
	'''

	r = originDist(x, y, z)
	theta = np.arctan2(y, x)
	phi = np.arcsin(z / r)

	position = (r, theta, phi)

	return position

def vectorAddition(vec_a, vec_b):
	''' Vector addition function (in 3D space). 

		Arguments:
			vec_a: [tuple of floats] First vector. 
			vec_b: [tuple of floats] Second vector. 

		Return:
			vec_c: [tuple of floats] The vector sum. 
	'''

	x_a = vec_a[0]
	y_a = vec_a[1]
	z_a = vec_a[2]

	x_b = vec_b[0]
	y_b = vec_b[1]
	z_b = vec_b[2]

	x_c = x_a + x_b
	y_c = y_a + y_b
	z_c = z_a + z_b

	vec_c = (x_c, y_c, z_c)

	return vec_c