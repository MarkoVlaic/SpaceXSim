''' Tools for performing the transformations of coordinates of spatial coordinate systems. '''

import numpy as np
import LinearAlgebra as linalg
import InitialParameters as init

def geocentricR(lat):
	''' Calculates the distance from the Earth's centre given a latitude and object height. 
		
		Arguments:
			lat: [float] Latitude of the object (rad).
			h: [float] Height of the object from the Earth's surface. (m)

		Returns:
			Rh: [float] The distance of the object from the Earth's centre. (m)
	'''

	# Calculate the distance 
	R = np.sqrt(((init.Earth.equat**2 * np.cos(lat))**2 + (init.Earth.polr**2 * np.sin(lat))**2) \
		/ ((init.Earth.equat * np.cos(lat))**2 + (init.Earth.polr * np.sin(lat))**2))
	
	return R


def geodeticToCartesian(lat, lon, h):
	''' Converts the geodesic Earth coordinates to coordinates in the Cartesian coordinate system
		(with its center as the system's origin).



		Arguments:
			lat: [float] Latitude of the object (rad).
			lon: [float] Longitude of the object (rad).
			h: [float] Height of the object from the Earth's surface. (m)

		Returns:
			position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object. (m, m, m)
	'''			

	# Get distance from the Earth's centre
	R = geocentricR(lat)

	# Calculate Cartesian coordinates
	x = (R + h) * np.cos(lat) * np.cos(lon)
	y = (R + h) * np.cos(lat) * np.sin(lon)
	z = (R + h) * np.sin(lat)

	position = (x, y, z)
	
	return position


def cartesianToGeodetic(x, y, z):
	''' Converts the Cartesian positional coordinates to geodesic coordinates. 
		Implemented according to (Bowring, 1985.). 

		Arguments:
			x: [float] X coordinate of the 3D position (m).
			y: [float] Y coordinate of the 3D position (m).
			z: [float] Z coordinate of the 3D position (m).

		Returns:
			position: [tuple of floats] A tuple of (lat, lon, h) geodesic coordinates of the object. 
	'''

	# Planar and 3D distances
	p = np.sqrt(x**2 + y**2)
	r = np.sqrt(x**2 + y**2 + z**2)
	
	# Angle chasing
	tu = init.Earth.polr * z * (1 + init.Earth.d/r) / (init.Earth.equat * p)
	cu3 = 1 / np.sqrt(1 + tu**2)**3
	tp = (z + init.Earth.d * cu3 * tu**3) / (p - init.Earth.ecc_sqr * init.Earth.equat * cu3)
	cp = 1 / np.sqrt(1 + tp**2)

	# Calculate final coordinates
	lat = np.arctan(tp)
	lon = np.arctan(y / x)
	h = p * cp + z * cp * tp - init.Earth.equat*np.sqrt(1 - init.Earth.ecc_sqr*(cp * tp)**2)

	position = (lat, lon, h)

	return position


def getHeight(x, y, z):
	''' Calculates the height of a point from the Earth's surface given that point's position.

		Arguments:
			x: [float] X coordinate of the 3D position (m).
			y: [float] Y coordinate of the 3D position (m).
			z: [float] Z coordinate of the 3D position (m).

		Returns:
			h: [float] Height of the object from the Earth's surface. (m)
	'''

	# Get latitude of a given position
	lat = cartesianToGeodetic(x, y, z)[0]
	
	# Get the radius of the Earth 
	earth_radius = geocentricR(lat)
	radius = linalg.originDist(x, y, z)

	height = radius - earth_radius

	return height


if __name__ == '__main__':

	### Testing ###
	# print(geocentricR(0))

	lat_init = 20	
	lon_init = 320
	h_init = 23.654

	lat_init = np.deg2rad(lat_init)
	lon_init = np.deg2rad(lon_init)

	x, y, z = geodeticToCartesian(lat_init, lon_init, h_init)
	lat, lon, h = cartesianToGeodetic(x, y, z)
	lat, lon = map(np.rad2deg, [lat, lon])

	print('Initial geodesic coordinates: {:.2f}, {:.2f}, {:.2f}'.format(lat_init, lon_init, h_init))
	print('Calculated Cartesbian coordinates: ' '{:1.4e},'.format(x), '{:1.4e},'.format(y), '{:1.4e}'.format(z))
	print('After transformation from Cartesian to geodesic: {:.2f}, {:.2f}, {:.2f}'.format(lat, lon, h))

	print('Distance from origin - geocentric radius at a calculated latitude:')
	print(getHeight(x, y, z))
