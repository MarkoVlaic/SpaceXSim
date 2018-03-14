''' A set of functions used for calculating the forces exerted on the rocket. '''

import numpy as np 
import scipy.constants as const 

# Earth's mass (in kg)
EARTH_MASS = 5.9722e24

def gravity(position, rocket_mass):
	''' Calculates the gravitational force on the rocket at any point. 

	Arguments:
		position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object.
		rocket mass: [float] The rocket's mass (in kg).

	Return:
		F: [tuple of floats] The force of gravity, split into components.
	'''

	# Unpack values from position tuple
	x = position[0]
	y = position[1]
	z = position[2]

	# Calculate distance from the center of the Earth at any time
	r = np.sqrt(x**2 + y**2 + z**2)

	# Calculate x, y, z components of the force of gravity
	Fx = (const.G * EARTH_MASS * rocket_mass) / r * x
	Fy = (const.G * EARTH_MASS * rocket_mass) / r * y
	Fz = (const.G * EARTH_MASS * rocket_mass) / r * z

	F = (Fx, Fy, Fz)

	return F


