''' Tools for performing the transformations of coordinates of spatial coordinate systems. '''

import numpy as np


# Earth's polar and equatorial radii (in meters)
EARTH_POLR = 6356.7523e3
EARTH_EQR = 6378.1370e3


def geocentricRh(lat, h):
	''' Calculates the distance from the Earth's centre given a latitude and object height. 
		
		Arguments:
			lat: [float] Latitude of the object (rad).
			h: [float] Height of the object from the Earth's surface.

		Return:
			Rh: [float] The distance of the object from the Earth's centre. 
	'''

	# Calculate the distance 
	rh = np.sqrt(((EARTH_EQR**2 * np.cos(lat))**2 + (EARTH_POLR**2 * np.sin(lat))**2) \
		/ ((EARTH_EQR * np.cos(lat))**2 + (EARTH_POLR * np.sin(lat))**2)) + h
	
	return rh 

def geodesicToXYZ(lat, lon, h):
	''' Converts the geodesic Earth coordinates to coordinates in the Cartesian coordinate system
		(with its center as the system's origin)

		Arguments:
			lat: [float] Latitude of the object (deg).
			lon: [float] Longitude of the object (deg).
			h: [float] Height of the object from the Earth's surface.

		Return:
			(x, y, z): [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object. 
	'''			


	# Convert to radians
	lat = np.deg2rad(lat)
	lon = np.deg2rad(lon)

	# Get distance from the Earth's centre
	rh = geocentricRh(lat, h)

	# Calculate Cartesian coordinates
	x = rh * np.cos(lat) * np.cos(lon)
	y = rh * np.cos(lat) * np.sin(lon)
	z = rh * np.sin(lat)

	return (x, y, z)

if __name__ == '__main__':

	### Testing ###
	print(geocentricRh(0, 0))

	x, y, z = geodesicToXYZ(10, 0, 10)

	print('{0:1.4e}'.format(x), '{0:1.4e}'.format(y), '{0:1.4e}'.format(z))