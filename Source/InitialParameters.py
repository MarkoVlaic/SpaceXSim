''' A set of functions used to describe the initial parameters pf the rocket. '''

import numpy as np
import scipy.constants as const

EARTH_POLR = 6356.7523e3
EARTH_MASS = 5.9722e24

def getVel(height):

	return np.sqrt(const.G * EARTH_MASS / (EARTH_POLR + height))

def getMass(payoload_mass, exhaust_velocity, height, k):

	return np.exp(getVel(height)/exhaust_velocity) * payoload_mass * (k + 1)

