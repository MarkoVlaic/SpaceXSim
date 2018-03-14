''' Tools for performing the transformations of coordinates of spatial coordinate systems. '''

import numpy as np
import LinearAlgebra as linalg


# Earth's polar and equatorial radii (in meters)
EARTH_POLR = 6356.7523e3
EARTH_EQR = 6378.1370e3

# Second eccentricity squared - the Earth is considered as an ellipsoid
ECC_SQR = 1 - (EARTH_POLR / EARTH_EQR)**2
SEC_ECC_SQR = ECC_SQR / (1 - ECC_SQR)
D = SEC_ECC_SQR * EARTH_POLR


def geocentricR(lat):
	''' Calculates the distance from the Earth's centre given a latitude and object height. 
		
		Arguments:
			lat: [float] Latitude of the object (rad).
			h: [float] Height of the object from the Earth's surface.

		Returns:
			Rh: [float] The distance of the object from the Earth's centre. 
	'''

	# Calculate the distance 
	R = np.sqrt(((EARTH_EQR**2 * np.cos(lat))**2 + (EARTH_POLR**2 * np.sin(lat))**2) \
		/ ((EARTH_EQR * np.cos(lat))**2 + (EARTH_POLR * np.sin(lat))**2))
	
	return R


def geodeticToCartesian(lat, lon, h):
	''' Converts the geodesic Earth coordinates to coordinates in the Cartesian coordinate system
		(with its center as the system's origin).

		Arguments:
			lat: [float] Latitude of the object (deg).
			lon: [float] Longitude of the object (deg).
			h: [float] Height of the object from the Earth's surface. (m)

		Returns:
			position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object. 
	'''			

	# Convert to radians
	lat = np.deg2rad(lat)
	lon = np.deg2rad(lon)

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
	tu = EARTH_POLR * z * (1 + D/r) / (EARTH_EQR * p)
	cu3 = 1 / np.sqrt(1 + tu**2)**3
	tp = (z + D * cu3 * tu**3) / (p - ECC_SQR * EARTH_EQR * cu3)
	cp = 1 / np.sqrt(1 + tp**2)

	# Calculate final coordinates
	lat = np.arctan(tp)
	lon = np.arctan2(y, x)
	h = p * cp + z * cp * tp - EARTH_EQR*np.sqrt(1 - ECC_SQR*(cp * tp)**2)

	position = (lat, lon, h)

	return position


def getHeight(x, y, z):
	''' Calculates the height of a point from the Earth's surface given that point's position.

		Arguments:
			x: [float] X coordinate of the 3D position (m).
			y: [float] Y coordinate of the 3D position (m).
			z: [float] Z coordinate of the 3D position (m).

		Returns:
			h: [float] Height of the object from the Earth's surface.
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

	lat_init = 10
	lon_init = 20
	h_init = 0

	x, y, z = geodeticToCartesian(lat_init, lon_init, h_init)
	lat, lon, h = map(np.rad2deg, cartesianToGeodetic(x, y, z))

	print('Initial geodesic coordinates: {:.2f}, {:.2f}, {:.2f}'.format(lat_init, lon_init, h_init))
	print('Calculated Cartesian: {0:1.4e}, {0:1.4e}, {0:1.4e}'.format(x, y, z))
	print('After transformation from Cartesian to geodesic: {:.2f}, {:.2f}, {:.2f}'.format(lat, lon, h))

	print('Distance from origin - geocentric radius at a calculated latitude:')
	print(getHeight(x, y, z))